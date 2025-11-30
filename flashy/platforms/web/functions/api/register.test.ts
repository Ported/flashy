import { describe, it, expect } from "vitest";
import { containsBlockedWord } from "./register";

describe("containsBlockedWord", () => {
  describe("allows clean names", () => {
    const cleanNames = [
      "Alice",
      "Bob",
      "Player1",
      "CoolKid99",
      "MathWizard",
      "StarPlayer",
      "Emma",
      "Oskar",
      "test-user",
      "my_name",
      "John Doe",
    ];

    it.each(cleanNames)("allows '%s'", (name) => {
      expect(containsBlockedWord(name)).toBe(false);
    });
  });

  describe("blocks obvious bad words", () => {
    const badNames = [
      "badword_fuck",
      "SHIT",
      "ass123",
      "mybitch",
    ];

    it.each(badNames)("blocks '%s'", (name) => {
      expect(containsBlockedWord(name)).toBe(true);
    });
  });

  describe("blocks l33t speak variations", () => {
    const leetNames = [
      ["sh1t", "i->1 becomes shit"],
      ["a$$", "$->s becomes ass"],
      ["@ss", "@->a becomes ass"],
      ["5hit", "5->s becomes shit"],
    ];

    it.each(leetNames)("blocks '%s' (%s)", (name) => {
      expect(containsBlockedWord(name)).toBe(true);
    });

    it("does not block l33t that doesn't normalize to blocked word", () => {
      // f4ck normalizes to fack, which isn't in blocklist
      expect(containsBlockedWord("f4ck")).toBe(false);
      // fvck has no normalization rule for v->u
      expect(containsBlockedWord("fvck")).toBe(false);
    });
  });

  describe("blocks names with separators", () => {
    const separatedNames = [
      "f_u_c_k",
      "s-h-i-t",
      "as s",
    ];

    it.each(separatedNames)("blocks '%s'", (name) => {
      expect(containsBlockedWord(name)).toBe(true);
    });
  });

  describe("blocks Swedish bad words", () => {
    const swedishBadNames = [
      "fitta",
      "FITTA",
      "kuk",
      "knulla",
    ];

    it.each(swedishBadNames)("blocks '%s'", (name) => {
      expect(containsBlockedWord(name)).toBe(true);
    });
  });

  describe("case insensitive", () => {
    it("blocks uppercase", () => {
      expect(containsBlockedWord("SHIT")).toBe(true);
    });

    it("blocks mixed case", () => {
      expect(containsBlockedWord("ShIt")).toBe(true);
    });
  });

  describe("blocks substrings", () => {
    it("blocks bad word at start", () => {
      expect(containsBlockedWord("shithead")).toBe(true);
    });

    it("blocks bad word at end", () => {
      expect(containsBlockedWord("bullshit")).toBe(true);
    });

    it("blocks bad word in middle", () => {
      expect(containsBlockedWord("myshitname")).toBe(true);
    });
  });
});
