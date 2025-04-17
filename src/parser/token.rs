use core::fmt;

pub struct Token {
    pub kind: TokenKind,
    pub start: usize,
    pub len: usize,
    pub text: String,
    pub line: usize,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}='{}'", self.kind, self.text)
    }
}

#[derive(Debug, Clone, Copy)]
pub enum TokenKind {
    // Common/misc symbols
    Comma,
    Colon,
    Semicolon,
    Pointer,
    OpenParen,
    CloseParen,
    OpenBracket,
    CloseBracket,
    OpenCurly,
    CloseCurly,
    Backslash,
    Hashtag,
    At,
    Eq,
    // Operators
    OpDot,
    OpNot,
    OpAnd,
    OpOr,
    OpEq,
    OpNeq,
    OpGt,
    OpGtEq,
    OpLt,
    OpLtEq,
    OpInc,
    OpDec,
    OpAdd,
    OpSub,
    OpMul,
    OpDiv,
    OpMod,
    // Keywords
    KwUse,
    KwRec,
    KwFun,
    KwVar,
    KwLet,
    KwRet,
    KwRaw,
    KwIf,
    KwElse,
    KwFor,
    KwEach,
    KwOf,
    KwNew,
    KwRef,
    KwAs,
    KwTo,
    KwIn,
    KwDef,
    KwMac,
    KwLit,
    KwTag,
    KwSwitch,
    KwCase,
    KwFall,
    // Literals
    True,
    False,
    Float,
    Int,
    Hex,
    Binary,
    Identifier,
    String,
    Character,
}
