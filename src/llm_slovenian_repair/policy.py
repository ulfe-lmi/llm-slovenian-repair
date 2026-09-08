"""Versioned, bounded policy configuration for future repair work."""

from __future__ import annotations

from math import isfinite
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    model_validator,
)

from .contracts import RepairMode

PolicyPositiveInt = Annotated[StrictInt, Field(gt=0)]
PolicyNonNegativeInt = Annotated[StrictInt, Field(ge=0)]
PolicyPositiveFloat = Annotated[StrictFloat, Field(gt=0)]


POLICY_CONFIG = ConfigDict(
    extra="forbid",
    frozen=True,
    strict=True,
    validate_assignment=True,
    validate_default=True,
    allow_inf_nan=False,
)


class PolicyConfig(BaseModel):
    """Conservative v1 limits; validation never reads environment or files."""

    model_config = POLICY_CONFIG

    schema_version: StrictInt = 1
    mode: RepairMode = RepairMode.DETECT_ONLY

    max_review_requests: PolicyPositiveInt = 1
    max_generative_passes: PolicyPositiveInt = 1
    max_automatic_retries: PolicyNonNegativeInt = 0
    max_concurrent_reviews: PolicyPositiveInt = 1
    max_targets: PolicyPositiveInt = 8
    max_target_words: PolicyPositiveInt = 6
    max_replacement_words: PolicyPositiveInt = 8

    max_target_code_points: PolicyPositiveInt = 128
    max_target_bytes: PolicyPositiveInt = 512
    max_replacement_code_points: PolicyPositiveInt = 160
    max_replacement_bytes: PolicyPositiveInt = 640
    max_safe_capture_code_points: PolicyPositiveInt = 32_768
    max_safe_capture_bytes: PolicyPositiveInt = 131_072
    max_analysis_code_points: PolicyPositiveInt = 32_768
    max_analysis_bytes: PolicyPositiveInt = 131_072
    max_context_code_points: PolicyPositiveInt = 512
    max_context_bytes: PolicyPositiveInt = 2_048
    max_prompt_code_points: PolicyPositiveInt = 16_384
    max_prompt_bytes: PolicyPositiveInt = 65_536
    max_review_output_code_points: PolicyPositiveInt = 8_192
    max_review_output_bytes: PolicyPositiveInt = 32_768
    max_queue_depth: PolicyPositiveInt = 16
    max_queue_wait_seconds: PolicyPositiveFloat = 2.0
    max_review_duration_seconds: PolicyPositiveFloat = 30.0

    allow_evidence_insufficient_acceptance: StrictBool = False
    persist_production_text: StrictBool = False
    enable_experimental_repair: StrictBool = False

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        if self.schema_version != 1:
            raise ValueError("only policy schema_version 1 is supported")
        if self.mode is RepairMode.EXPERIMENTAL or self.enable_experimental_repair:
            raise ValueError("experimental repair is not enabled in policy schema version 1")

        maxima = {
            "max_review_requests": 1,
            "max_generative_passes": 1,
            "max_automatic_retries": 0,
            "max_concurrent_reviews": 1,
            "max_targets": 8,
            "max_target_words": 6,
            "max_replacement_words": 8,
        }
        for name, maximum in maxima.items():
            if getattr(self, name) > maximum:
                raise ValueError(f"{name} exceeds the architecture maximum")
        if self.allow_evidence_insufficient_acceptance or self.persist_production_text:
            raise ValueError(
                "v1 forbids evidence-insufficient acceptance and production text storage"
            )

        byte_pairs = (
            (self.max_target_bytes, self.max_target_code_points, "target"),
            (self.max_replacement_bytes, self.max_replacement_code_points, "replacement"),
            (self.max_safe_capture_bytes, self.max_safe_capture_code_points, "safe capture"),
            (self.max_analysis_bytes, self.max_analysis_code_points, "analysis"),
            (self.max_context_bytes, self.max_context_code_points, "context"),
            (self.max_prompt_bytes, self.max_prompt_code_points, "prompt"),
            (self.max_review_output_bytes, self.max_review_output_code_points, "review output"),
        )
        for byte_limit, code_point_limit, label in byte_pairs:
            if byte_limit < code_point_limit:
                raise ValueError(f"{label} byte limit must cover its code-point limit")

        if self.max_analysis_code_points > self.max_safe_capture_code_points:
            raise ValueError("analysis code-point limit exceeds safe capture limit")
        if self.max_analysis_bytes > self.max_safe_capture_bytes:
            raise ValueError("analysis byte limit exceeds safe capture limit")
        minimum_prompt = self.max_targets * (
            self.max_target_code_points + (2 * self.max_context_code_points)
        )
        if self.max_prompt_code_points < minimum_prompt:
            raise ValueError("prompt code-point limit cannot hold bounded targets and context")
        if self.max_prompt_bytes < self.max_targets * (
            self.max_target_bytes + (2 * self.max_context_bytes)
        ):
            raise ValueError("prompt byte limit cannot hold bounded targets and context")
        if self.max_review_duration_seconds < self.max_queue_wait_seconds:
            raise ValueError("review duration must cover queue wait")
        for name in ("max_queue_wait_seconds", "max_review_duration_seconds"):
            if not isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        return self


Policy = PolicyConfig


__all__ = ["Policy", "PolicyConfig"]
