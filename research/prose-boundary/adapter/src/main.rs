//! MEASUREMENT ADAPTER — objective 008, round 008-a (research-only).
//!
//! This binary is a MEASUREMENT ADAPTER, not a runtime interface. It reads one
//! complete document from stdin, parses it with the pinned candidate
//! `pulldown-cmark` 0.13.4 (crates.io registry checksum
//! e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e; upstream
//! pulldown-cmark/pulldown-cmark tag v0.13.4), and emits one deterministic
//! JSON line per event:
//!
//!   {"i":<u64>,"k":"<kind token>","s":<start_byte>,"e":<end_byte>}
//!
//! followed by `{"eof":true}`. Offsets are BYTE offsets into the original
//! input bytes (UTF-8), exactly as produced by the candidate's
//! `Parser::into_offset_iter()`; this adapter adds no transformation.
//!
//! Frozen profiles (research/prose-boundary/config/experiment-008a.json):
//!   P0 = CommonMark core (Options::empty())
//!   P1 = P0 + ENABLE_TABLES | ENABLE_STRIKETHROUGH | ENABLE_TASKLISTS | ENABLE_MATH
//!   P2 = P1 + ENABLE_YAML_STYLE_METADATA_BLOCKS
//!
//! No event content is emitted: the original document is the source of
//! content and only kinds plus byte ranges are measured.
//!
//! Exit codes: 0 = OK; 3 = stdin not valid UTF-8 (emits {"invalid_utf8":true});
//! 5 = usage error or write failure.

use std::borrow::Cow;
use std::io::{Read, Write};

use pulldown_cmark::{CodeBlockKind, Event, Options, Parser, Tag, TagEnd};

fn main() {
    let mut args = std::env::args().skip(1);
    let profile = match args.next() {
        Some(p) => p,
        None => {
            eprintln!("usage: prose-boundary-meas <P0|P1> < document");
            std::process::exit(5);
        }
    };
    if args.next().is_some() {
        eprintln!("unexpected extra argument");
        std::process::exit(5);
    }
    let options = match profile.as_str() {
        "P0" => Options::empty(),
        "P1" => Options::empty()
            | Options::ENABLE_TABLES
            | Options::ENABLE_STRIKETHROUGH
            | Options::ENABLE_TASKLISTS
            | Options::ENABLE_MATH,
        "P2" => Options::empty()
            | Options::ENABLE_TABLES
            | Options::ENABLE_STRIKETHROUGH
            | Options::ENABLE_TASKLISTS
            | Options::ENABLE_MATH
            | Options::ENABLE_YAML_STYLE_METADATA_BLOCKS,
        other => {
            eprintln!("unknown profile: {other}");
            std::process::exit(5);
        }
    };
    let mut input = Vec::new();
    if std::io::stdin().read_to_end(&mut input).is_err() {
        eprintln!("stdin read error");
        std::process::exit(5);
    }
    let text = match std::str::from_utf8(&input) {
        Ok(t) => t,
        Err(_) => {
            let _ = writeln!(std::io::stdout(), "{{\"invalid_utf8\":true}}");
            std::process::exit(3);
        }
    };
    let mut parser = Parser::new_ext(text, options).into_offset_iter();
    let stdout = std::io::stdout();
    let mut out = std::io::BufWriter::new(stdout.lock());
    let mut idx: u64 = 0;
    while let Some((event, range)) = parser.next() {
        let kind = kind_token(&event);
        let line = format!(
            "{{\"i\":{},\"k\":\"{}\",\"s\":{},\"e\":{}}}\n",
            idx, kind, range.start, range.end
        );
        if out.write_all(line.as_bytes()).is_err() {
            eprintln!("stdout write error");
            std::process::exit(5);
        }
        idx += 1;
    }
    if out.write_all(b"{\"eof\":true}\n").is_err() || out.flush().is_err() {
        eprintln!("stdout write error");
        std::process::exit(5);
    }
}

/// Frozen kind tokens. Every 0.13.4 Event variant is covered; the trailing
/// arm is unreachable and fails loudly if the pinned API ever differs.
fn kind_token(ev: &Event) -> Cow<'static, str> {
    let borrowed = |s: &'static str| Cow::Borrowed(s);
    match ev {
        Event::Start(tag) => match tag {
            Tag::Paragraph => borrowed("S.Para"),
            Tag::Heading { level, .. } => Cow::Owned(format!("S.Head:{}", *level as u64)),
            Tag::BlockQuote(_) => borrowed("S.Quote"),
            Tag::CodeBlock(CodeBlockKind::Fenced(_)) => borrowed("S.CodeBlock:Fenced"),
            Tag::CodeBlock(CodeBlockKind::Indented) => borrowed("S.CodeBlock:Indented"),
            Tag::HtmlBlock => borrowed("S.HtmlBlock"),
            Tag::List(Some(n)) => Cow::Owned(format!("S.List:ol:{n}")),
            Tag::List(None) => borrowed("S.List:ul"),
            Tag::Item => borrowed("S.Item"),
            Tag::FootnoteDefinition(_) => borrowed("S.FootnoteDef"),
            Tag::DefinitionList => borrowed("S.DefList"),
            Tag::DefinitionListTitle => borrowed("S.DefTitle"),
            Tag::DefinitionListDefinition => borrowed("S.DefDef"),
            Tag::Table(_) => borrowed("S.Table"),
            Tag::TableHead => borrowed("S.TableHead"),
            Tag::TableRow => borrowed("S.TableRow"),
            Tag::TableCell => borrowed("S.TableCell"),
            Tag::Emphasis => borrowed("S.Emph"),
            Tag::Strong => borrowed("S.Strong"),
            Tag::Strikethrough => borrowed("S.Strike"),
            Tag::Superscript => borrowed("S.Sup"),
            Tag::Subscript => borrowed("S.Sub"),
            Tag::Link { .. } => borrowed("S.Link"),
            Tag::Image { .. } => borrowed("S.Image"),
            Tag::MetadataBlock(_) => borrowed("S.Meta"),
        },
        Event::End(end) => match end {
            TagEnd::Paragraph => borrowed("E.Para"),
            TagEnd::Heading(level) => Cow::Owned(format!("E.Head:{}", *level as u64)),
            TagEnd::BlockQuote(_) => borrowed("E.Quote"),
            TagEnd::CodeBlock => borrowed("E.CodeBlock"),
            TagEnd::HtmlBlock => borrowed("E.HtmlBlock"),
            TagEnd::List(true) => borrowed("E.List:ol"),
            TagEnd::List(false) => borrowed("E.List:ul"),
            TagEnd::Item => borrowed("E.Item"),
            TagEnd::FootnoteDefinition => borrowed("E.FootnoteDef"),
            TagEnd::DefinitionList => borrowed("E.DefList"),
            TagEnd::DefinitionListTitle => borrowed("E.DefTitle"),
            TagEnd::DefinitionListDefinition => borrowed("E.DefDef"),
            TagEnd::Table => borrowed("E.Table"),
            TagEnd::TableHead => borrowed("E.TableHead"),
            TagEnd::TableRow => borrowed("E.TableRow"),
            TagEnd::TableCell => borrowed("E.TableCell"),
            TagEnd::Emphasis => borrowed("E.Emph"),
            TagEnd::Strong => borrowed("E.Strong"),
            TagEnd::Strikethrough => borrowed("E.Strike"),
            TagEnd::Superscript => borrowed("E.Sup"),
            TagEnd::Subscript => borrowed("E.Sub"),
            TagEnd::Link => borrowed("E.Link"),
            TagEnd::Image => borrowed("E.Image"),
            TagEnd::MetadataBlock(_) => borrowed("E.Meta"),
        },
        Event::Text(_) => borrowed("Text"),
        Event::Code(_) => borrowed("Code"),
        Event::InlineMath(_) => borrowed("InlineMath"),
        Event::DisplayMath(_) => borrowed("DisplayMath"),
        Event::Html(_) => borrowed("Html"),
        Event::InlineHtml(_) => borrowed("InlineHtml"),
        Event::FootnoteReference(_) => borrowed("FootnoteRef"),
        Event::SoftBreak => borrowed("SoftBreak"),
        Event::HardBreak => borrowed("HardBreak"),
        Event::Rule => borrowed("Rule"),
        Event::TaskListMarker(_) => borrowed("TaskListMarker"),
        other => Cow::Owned(format!("UNEXPECTED:{other:?}")),
    }
}
