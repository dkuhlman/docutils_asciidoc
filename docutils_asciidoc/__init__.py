"""
    docutils_asciidoc
    ~~~~~~~~~~~~~~~~~

    Asciidoc parser for docutils.

    :copyright: Copyright 2022 by Dave Kuhlman
    :license: Apache License 2.0, see LICENSE for details.
"""

from typing import List, Type

from docutils import nodes
from docutils.parsers import Parser
from docutils.transforms import Transform

from docutils_asciidoc.blockparser import BlockParser, BlockProcessor
from docutils_asciidoc.blockparser.container_processors import (
    BlockQuoteProcessor,
    BulletListProcessor,
    NonEmptyBulletListProcessor,
    OneBasedOrderedListProcessor,
    OrderedListProcessor,
)
from docutils_asciidoc.blockparser.html_processors import (
    CdataHTMLBlockProcessor,
    CommentHTMLBlockProcessor,
    CompleteTagsHTMLBlockProcessor,
    DeclarationHTMLBlockProcessor,
    ProcessingInstructionHTMLBlockProcessor,
    ScriptHTMLBlockProcessor,
    StandardTagsHTMLBlockProcessor,
)
from docutils_asciidoc.blockparser.link_processors import (
    LinkReferenceDefinitionProcessor
)
from docutils_asciidoc.blockparser.std_processors import (
    ATXHeadingProcessor,
    BacktickFencedCodeBlockProcessor,
    BlankLineProcessor,
    IndentedCodeBlockProcessor,
    ParagraphProcessor,
    SetextHeadingProcessor,
    ThematicBreakProcessor,
    TildeFencedCodeBlockProcessor,
)
from docutils_asciidoc.inlineparser import InlineProcessor
from docutils_asciidoc.inlineparser.link_processors import (
    LinkCloserProcessor,
    LinkOpenerProcessor,
)
from docutils_asciidoc.inlineparser.std_processors import (
    BackslashEscapeProcessor,
    CodeSpanProcessor,
    EmailAutolinkProcessor,
    EmphasisProcessor,
    EntityReferenceProcessor,
    HardLinebreakProcessor,
    RawHTMLProcessor,
    SoftLinebreakProcessor,
    URIAutolinkProcessor,
)
from docutils_asciidoc.readers import LineReader
from docutils_asciidoc.transforms import (
    BlanklineFilter,
    BracketConverter,
    EmphasisConverter,
    InlineTransform,
    LinebreakFilter,
    SectionTreeConstructor,
    SparseTextConverter,
    TextNodeConnector,
    TightListsCompactor,
    TightListsDetector,
)


class CommonMarkParser(Parser):
    """CommonMark parser for docutils."""

    supported = ('markdown', 'commonmark', 'md')

    def get_block_processors(self) -> List[Type[BlockProcessor]]:
        """Returns block processors. Overrided by subclasses."""
        return [
            ATXHeadingProcessor,
            BacktickFencedCodeBlockProcessor,
            BlankLineProcessor,
            BlockQuoteProcessor,
            BulletListProcessor,
            CdataHTMLBlockProcessor,
            CommentHTMLBlockProcessor,
            CompleteTagsHTMLBlockProcessor,
            DeclarationHTMLBlockProcessor,
            IndentedCodeBlockProcessor,
            LinkReferenceDefinitionProcessor,
            NonEmptyBulletListProcessor,
            OneBasedOrderedListProcessor,
            OrderedListProcessor,
            ParagraphProcessor,
            ProcessingInstructionHTMLBlockProcessor,
            ScriptHTMLBlockProcessor,
            SetextHeadingProcessor,
            StandardTagsHTMLBlockProcessor,
            ThematicBreakProcessor,
            TildeFencedCodeBlockProcessor,
        ]

    def get_inline_processors(self) -> List[Type[InlineProcessor]]:
        """Returns inline processors. Overrided by subclasses."""
        return [
            BackslashEscapeProcessor,
            CodeSpanProcessor,
            EmailAutolinkProcessor,
            EmphasisProcessor,
            EntityReferenceProcessor,
            HardLinebreakProcessor,
            LinkCloserProcessor,
            LinkOpenerProcessor,
            RawHTMLProcessor,
            SoftLinebreakProcessor,
            URIAutolinkProcessor,
        ]

    def get_transforms(self) -> List[Type[Transform]]:
        return [
            BlanklineFilter,
            BracketConverter,
            EmphasisConverter,
            InlineTransform,
            LinebreakFilter,
            SectionTreeConstructor,
            SparseTextConverter,
            TextNodeConnector,
            TightListsCompactor,
            TightListsDetector,
        ]

    def create_block_parser(self) -> BlockParser:
        """Creates a block parser and returns it.

        Internally, ``get_block_processors()`` is called to create a parser.
        So you can change the processors by subclassing.
        """
        parser = BlockParser()
        for processor in self.get_block_processors():
            parser.add_processor(processor(parser))
        return parser

    def parse(self, inputtext: str, document: nodes.document) -> None:
        """Parses a text and build document."""
        document.settings.inline_processors = self.get_inline_processors()
        reader = LineReader(inputtext.splitlines(True), source=document['source'])
        block_parser = self.create_block_parser()
        block_parser.parse(reader, document)
