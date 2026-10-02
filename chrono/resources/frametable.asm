; BANK_FRAMETABLE.asm
; Created by Banker v1.00

FrameTable

;             Bank  <Frame Address         >Frame Address              #

 .byte FRAMEBANK00, <    FRAME_BLUE_png_0, >    FRAME_BLUE_png_0  ;   0
FRAME_BLUE = 0
 .byte FRAMEBANK00, <   FRAME_GREEN_png_1, >   FRAME_GREEN_png_1  ;   1
FRAME_GREEN = 1
 .byte FRAMEBANK00, <     FRAME_RED_png_2, >     FRAME_RED_png_2  ;   2
FRAME_RED = 2


FRAMECOUNT = 3

; END
