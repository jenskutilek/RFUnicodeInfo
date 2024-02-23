from __future__ import annotations

# Unicode Info
# An extension for the RoboFont editor
# Version 0.1 by Jens Kutilek 2016-10-24
# Version 1.0 by Jens Kutilek 2017-01-19
# Version 1.2 by Jens Kutilek 2018-03-29
# Version 2.1 by Jens Kutilek 2021-10-16
# Version 2.2 by Jens Kutilek 2021-10-18

from glyphNameFormatter import GlyphName
from lib.tools.unicodeTools import getGlyphNameComponentUnicode
from jkUnicode.aglfn import getGlyphnameForUnicode, getUnicodeForGlyphname
from unicodeInfoWindow import UnicodeInfoWindow

from mojo.roboFont import CurrentFont, CurrentGlyph
from mojo.subscriber import Subscriber, WindowController
from mojo.UI import SetCurrentGlyphByName


class UnicodeInfoUI(UnicodeInfoWindow, Subscriber, WindowController):
    def build(self):
        self.build_window()
        self.glyph = CurrentGlyph()

    @property
    def font_fallback(self):
        if self._font is not None:
            return self._font
        return CurrentFont()

    @property
    def font_glyphs(self):
        if self._font is not None:
            return self._font
        return []

    @property
    def glyph_font(self):
        if self._glyph is None:
            return None

        return self._glyph.font

    @property
    def glyph_unicode(self):
        if self._glyph is None:
            return None
        if self._glyph.unicode is None:
            return None

        return self._glyph.unicode

    def glyphs_for_font(self, font):
        if font is None:
            return {}
        return self._font

    def get_unicode_for_glyphname(self, name=None):
        if name is None:
            return None
        # First try jkUnicode
        u = getUnicodeForGlyphname(name)
        if u is None:
            # then try GNFUL
            u = getGlyphNameComponentUnicode(name)
            if u is not None:
                u = u[1]
        return u

    def gnful_name(self, u):
        return GlyphName(uniNumber=u).getName()

    def glyphDidChangeInfo(self, info):
        # print("glyphDidChangeInfo", info)
        self._updateGlyph()

    # def currentGlyphDidSetGlyph(self, info):
    #     print("currentGlyphDidSetGlyph", info)
    #     self.glyph = info["glyph"]
    #     self.font = self.glyph.font if self.glyph is not None else None
    #     self.view = info["lowLevelEvents"]["view"]
    #     self._updateGlyph()

    def roboFontDidSwitchCurrentGlyph(self, info):
        self.glyph = info["glyph"]
        self.font = self.glyph.font if self.glyph is not None else None
        self.view = info["lowLevelEvents"][0]["view"]
        self._updateGlyph()

    def _saveGlyphSelection(self, font=None):
        if font is None:
            font = self.font
        if font:
            self.selectedGlyphs = font.selectedGlyphNames
        else:
            self.selectedGlyphs = ()

    def _restoreGlyphSelection(self, font=None):
        if font is None:
            if self.font is None:
                return

            font = self.font
        font.selectedGlyphNames = self.selectedGlyphs

    def toggleCase(self, sender=None):
        if self.font is None:
            return

        glyphname = getGlyphnameForUnicode(self.case)
        if self.view is None:
            # No Glyph Window, use the selection in the Font Window
            self.font.selectedGlyphNames = [glyphname]
        else:
            # Show the cased glyph in the Glyph Window
            SetCurrentGlyphByName(glyphname)


if __name__ == "__main__":
    UnicodeInfoUI(currentGlyph=True)
