;------------------------------------------------------------------------------
; Interleaved Chronocolour Sprite Technology Demo
; Copyright (C)2003 Andrew Davie - adavie@atari2600.org
; Caution - master at work ;)

; This is the full source-code for the colour-sprite technology known as
; 'Interleaved Chronocolour'.  The system displays two 48 pixel wide x
; 128 pixel deep sprites in colour through the time-based interlacing of
; red/green/blue component frames of an original colour image.

; System and utilities developed by Andrew Davie during February/March 2003.
; As with many things, this system builds upon the work, ideas, and 
; suggestions of those who have come before.  Particular thanks and
; acknowledgement go to Eckhard Stohlberg, who shared his original large
; two-player sprite system, and to Thomas Jentzsch who developed alternate
; versions of technology and made many good suggestions as we moved towards
; a final solution to the challenge.  No man is an island.

; If you use this system for any purpose, I would appreciate a short note
; via email.  If you design/release a ROM using this system, then I would
; like acknowledgement in any manual/documentation of my contribution through
; this system.

; Hacked together by Chrono2.EXE

;------------------------------------------------------------------------------

                processor 6502

; Atari 2600 Equates

VSYNC   equ     $40             ;   0000 00x0       Vertical Sync Set-Clear
VBLANK  equ     $41             ;   xx00 00x0       Vertical Blank Set-Clear
WSYNC   equ     $42             ;   ---- ----       Wait for Horizontal Blank
NUSIZ0  equ     $44             ;   00xx 0xxx       Number-Size player/missle 0
NUSIZ1  equ     $45             ;   00xx 0xxx       Number-Size player/missle 1
COLUP0  equ     $46             ;   xxxx xxx0       Color-Luminance Player 0
COLUP1  equ     $47             ;   xxxx xxx0       Color-Luminance Player 1
COLUPF  equ     $48             ;   xxxx xxx0       Color-Luminance Playfield
COLUBK  equ     $49             ;   xxxx xxx0       Color-Luminance Background
CTRLPF  equ     $4A             ;   00xx 0xxx       Control Playfield, Ball, Collisions
REFP0   equ     $4B             ;   0000 x000       Reflection Player 0
REFP1   equ     $4C             ;   0000 x000       Reflection Player 1
PF0     equ     $4D             ;   xxxx 0000       Playfield Register Byte 0
PF1     equ     $4E             ;   xxxx xxxx       Playfield Register Byte 1
PF2     equ     $4F             ;   xxxx xxxx       Playfield Register Byte 2
RESP0   equ     $50             ;   ---- ----       Reset Player 0
RESP1   equ     $51             ;   ---- ----       Reset Player 1
GRP0    equ     $5B             ;   xxxx xxxx       Graphics Register Player 0
GRP1    equ     $5C             ;   xxxx xxxx       Graphics Register Player 1
HMP0    equ     $60             ;   xxxx 0000       Horizontal Motion Player 0
HMP1    equ     $61             ;   xxxx 0000       Horizontal Motion Player 1
VDELP0  equ     $65             ;   0000 000x       Vertical Delay Player 0
VDELP1  equ     $66             ;   0000 000x       Vertical Delay Player 1
HMOVE   equ     $6A             ;   ---- ----       Apply Horizontal Motion
HMCLR   equ     $6B             ;   ---- ----       Clear Horizontal Move Registers
 
SWACNT  equ     $281            ;                   Port A data direction register (DDR)
SWBCNT  equ     $283            ;                   Port B DDR
INTIM   equ     $284            ;                   Timer output
TIM64T  equ     $296            ;                   set 64 clock interval

;------------------------------------------------------------------------------


    ;------------------------------------------------------------------------------
    ; This binary can be compiled for ONE of PAL, NTSC, SECAM compatibility
    ; just set COLOUR = the one you want.  The values, by the way, coincidentally
    ; correspond to the -cN switch in Z26 (ie: -c0 = NTSC palette).

NTSC            = 0
PAL             = 1
SECAM           = 2

COLOUR          = NTSC      ; <-- change THIS to NTSC, PAL, or SECAM

    ;------------------------------------------------------------------------------

BASEY           = 45        ; lowest y-position for sprites (don't forget, sprites have
                            ; centerpoints, so this is the lowest Y for the top left
                            ; which is the centerpoint y-position of the frames in
                            ; this demo.

BGCOL           = 0         ; colour of background - black is best
PFCOL           = 0         ; colour of playfield.  None used in this demo

FRAMEBANK00     = 0         ; just required for BANKER-UTILITY produced  code

D0              = 1         ; bit values...
D1              = 2
D2              = 4
D3              = 8
D4              = 16
D5              = 32
D6              = 64
D7              = 128

;------------------------------------------------------------------------------
; Code automatically compiles to implement the sprites in the size/format
; specified here.  

; REDUNDANT:  BIG_ROWS comes from an earlier version of the sprite system which
; handled sprites in a matrix of rows and columns.  Just leave BIG_ROWS = 1 and
; BIG_COLS = 6, as the current system is pretty much reliant on these dimensions.

BIG_ROWS        = 1
BIG_COLS        = 6         ; DO NOT CHANGE

; You can have 1 or two creatures...

BIG_SPRITES     = 1         ; change to 1 or 2 as you wish

;------------------------------------------------------------------------------
; MACRO definitions 


    MAC VECTOR              ; just a word pointer to code
        .word {1}
    ENDM

    MAC ANIMATION
            lda #<{1}
            sta ObjAnimLO,x
            lda #>{1}
            sta ObjAnimHI,x
            lda #1
            sta ObjDelay,x

    ENDM

    MAC HANDLER
            ldy #{1}*2
            jsr SetHandler
    ENDM

    MAC STATE       ; does not continue after macro!

            ldy #STATE_{1}*2
            jmp SetState

    ENDM

;------------------------------------------------------------------------------

                SEG.U variables
                ORG $80

DrawX           ds 2
DrawY           ds 1
CenterX         ds 2
CenterY         ds 1

VisualX         ds 2
VisualY         ds 1

LoopCount       ds 1
SPBASE          ds BIG_ROWS * BIG_COLS * 2

BGColour        ds 1

Temp            ds 2
Anim            ds 2
RGBVec          ds 2

Player          ds 1
FrameAddress    ds 2
Phase           ds 1
gravity         ds BIG_SPRITES                ; used to bounce the player 
gravityinc      ds BIG_SPRITES

; Object variables

ObjXPosition    ds BIG_SPRITES
ObjYPosition    ds BIG_SPRITES

ObjFacing       ds BIG_SPRITES

                ; F-------
                ; F = facing direction (0 = right, 1 = left)
                ; - = unused

ObjDelay        ds BIG_SPRITES              ; delay count for frame animation
ObjAnimLO       ds BIG_SPRITES              ; animation pointer lo byte
ObjAnimHI       ds BIG_SPRITES              ; animation pointer hi byte
ObjStateLO      ds BIG_SPRITES              ; state table lo byte
ObjStateHI      ds BIG_SPRITES              ; state table hi byte
ObjFSMLO        ds BIG_SPRITES              ; FSM system lo byte
ObjFSMHI        ds BIG_SPRITES              ; FSM system hi byte
ObjFrame        ds BIG_SPRITES


;------------------------------------------------------------------------------

            SEG
            ORG $F000

    include "Bank00.asm"
  
;------------------------------------------------------------------------------



InitX
INXPOS  SET 80
    REPEAT BIG_SPRITES
    .byte INXPOS
INXPOS  SET INXPOS + 48
    REPEND

GIStart
    .byte 5,0,7,9,2,1,3


    ; There's no particular reason why this code lives in a separate bank
    ; but it's as good-a-test as any for checking the bankswitching is working


Reset 
Cart_Init
            sei
            cld
               
		    ldx #$FF
		    txs 				; Clear the stack

            lda #0
            sta SWBCNT          ; console I/O always set to INPUT
            sta SWACNT          ; set controller I/O to INPUT


            sta Player
            sta Phase

    ; Initialise creatures

            ldx #BIG_SPRITES-1
PreClear    

            lda #0
            sta ObjFacing,x
            sta gravity,x

            lda GIStart,x
            sta gravityinc,x


            lda #BASEY
            sta ObjYPosition,x

            lda InitX,x
            sta ObjXPosition,x

            ldy #STATE_NORMAL*2
            jsr SetState                    ; also calls processFSM
            HANDLER EVENT_INIT2

;            lda #D7
;            sta ObjFacing,x

            jsr AnimateObject               ; process object animation sequence

            dex
            bpl PreClear

    ;----------------------------------
    ; Hardwire init a single creature...

    #if BIG_SPRITES > 1

;            lda #D7
;            sta ObjFacing           ;todo currently fucked

;            ldx #1
;            HANDLER EVENT_INIT2

;            ldx #0
;            HANDLER 0

    #endif

;            ldx #0
;            HANDLER NORMAL_STAND
  

    ;----------------------------------


            lda #BGCOL
            sta BGColour

            jmp NewFrame


;------------------------------------------------------------------------------

    include "Bank_Frametable.asm"


;------------------------------------------------------------------------------
; OBJECT Animation


    MAC SHOW
            .byte {1},{2}
    ENDM

    MAC SHOWRGB
    REPEAT {2}
        SHOW FRAME_{1}RED,1
        SHOW FRAME_{1}GREEN,1
        SHOW FRAME_{1}BLUE,1
    REPEND
    ENDM

    MAC SYNCH
            .byte TOKEN_SYNCH
    ENDM
    
    MAC SETCOL
            .byte TOKEN_COLOUR
            .byte {1}
    ENDM

    MAC LOCK

            .byte TOKEN_LOCK
            .byte {1}*2

    ENDM


    MAC UNLOCK
            .byte TOKEN_UNLOCK
    ENDM

    MAC GOTO
            .byte TOKEN_JUMP
            .word {1}
    ENDM

	MAC DONE
			.byte TOKEN_DONE
	ENDM

    MAC MOVE
            .byte TOKEN_MOVE
            .word {1}
            .byte {2}
    ENDM

	MAC FLIP
			.byte TOKEN_FLIP
	ENDM



NOFRAME     equ $FF


noAnim      lda #NOFRAME
            sta ObjFrame,x
            rts


exitAnim    rts


AnimateObject


            lda ObjAnimHI,x
            beq noAnim                      ; animation switched off - use a null frame

            lda ObjDelay,x
            beq exitAnim                    ; static frame - no animation
            dec ObjDelay,x
            bne exitAnim                    ; not ready to change

ReAnimate   lda ObjAnimHI,x
            sta Anim+1
            lda ObjAnimLO,x
            sta Anim                        ; (Anim) points to frame sequence

ReReAnim    ldy #0
            lda (Anim),y
            bpl NormalFrame

            asl
            tay

            lda AnimVec,y
            sta Temp
            lda AnimVec+1,y
            sta Temp+1
            jmp (Temp)

    ;------------------------------------------------------------------------------
    ; Automatically define tokens and a vector table to token-processing code
    ; This is fairly neat, as the ordering of the entries in the table auto-generates
    ; the appropriate equates to access the table correctly!

TOK         SET 128
            MAC TOKEN
TOKEN_{1}   equ TOK
TOK         SET TOK + 1
            VECTOR Animate{1}
            ENDM

AnimVec     TOKEN JUMP
            TOKEN MOVE
            TOKEN FLIP
            TOKEN SYNCH

    ;------------------------------------------------------------------------------

AnimateFLIP

            lda ObjFacing,x
            eor #D7
            sta ObjFacing,x

			lda #1
			bne AnimUp


NormalFrame

            sta ObjFrame,x

            iny
            lda (Anim),y
            sta ObjDelay,x                  ; should be < 128

            clc
            lda Anim
            adc #2
            sta ObjAnimLO,x
            lda Anim+1
            adc #0
            sta ObjAnimHI,x
            rts

    ;------------------------------------------------------------------------------


AnimUp      clc
            adc Anim
            sta Anim
            bcc ReReAnim
            inc Anim+1
            bcs ReReAnim

    ;------------------------------------------------------------------------------


AnimateJUMP

                ; Handle a JUMP

            ldy #1
            lda (Anim),y
            sta ObjAnimLO,x
            iny
            lda (Anim),y
            sta ObjAnimHI,x
            jmp ReAnimate



    ;------------------------------------------------------------------------------

NewGravity

    .byte 0,0,-2,-4,-6,-8,-10,-8,-7,-5,-3,-1

GravityIncT
    .byte 1,2,3,4,5,6,7,8,9,10,0

            
AnimateMOVE

;            cpx #0
;            bne nog

            inc gravity,x

            clc
            lda DrawY
       ;     adc gravity,x
            cmp #BASEY
            bcc gOK

            ldy gravityinc,x
            lda GravityIncT,y
            sta gravityinc,x

            lda NewGravity,y
            sta gravity,x

            lda #BASEY
gOK         sta DrawY
nog

            lda ObjXPosition,x
            cmp #25
            bcs FR
            lda #D7
            sta ObjFacing,x
FR

            lda ObjXPosition,x
            cmp #160-25
            bcc FL
            lda #0
            sta ObjFacing,x
FL


            ldy #1

            lda (Anim),y
            sta Temp
            iny
            lda (Anim),y
            sta Temp+1

            lda ObjFacing,x
            bpl MoveRight

            sec
            lda #0
            sbc Temp
            sta Temp
            lda #0
            sbc Temp+1
            sta Temp+1

MoveRight

            clc
            adc DrawX
            adc Temp
            sta DrawX
            lda DrawX+1
            adc Temp+1
            sta DrawX+1

            iny
            lda (Anim),y
            clc
            adc DrawY
            sta DrawY

            clc
            lda Anim
            adc #4
            sta Anim
            lda Anim+1
            adc #0
            sta Anim+1

            jmp ReReAnim

AnimateSYNCH

#if BIG_SPRITES = 1
            lda #0
#else
            lda #2
#endif

            sta Phase
            lda #1
            jmp AnimUp

    ;------------------------------------------------------------------------------
    ; Animations processing code proceeds until it has a frame and duration
    ; The duration is in TV-frames, and counts down.  When 0, the next 'command' in the
    ; animation sequence is processed.  Animations must use the GOTO to halt or repeat
    ; Animations are tokenised interpreted little programs.

    ; Commands/Macros
    ;   GOTO label              Vector to the label
    ;   MOVE x,y                Adjust position by x,y pixels
    ;   FLIP                    Mirror creature
    ;   SHOW frame,delay        Set th creature rame and delay (also halts animation till delay counts to 0)


ANIMATION_STAND

        SYNCH                   ; Reset RGB phase to start

ANIMATION_STAND2

        SHOW FRAME_RED,1
        ;MOVE -1,0
        SHOW FRAME_GREEN,1
        ;MOVE -1,0
        SHOW FRAME_BLUE,1
        ;MOVE -1,0

        GOTO ANIMATION_STAND2


; OBJECT Animation END
;------------------------------------------------------------------------------
 

;------------------------------------------------------------------------------
; STATE Processing

SetState

    ; Set object's state base
    ; x = obj
    ; y = state table (*2)

            lda StateTables,y
            sta ObjStateLO,x
            lda StateTables+1,y
            sta ObjStateHI,x

            ldy #EVENT_DEFAULT*2                ; fall through and include DEFAULT init for handler

SetHandler

    ; Change object's processing code
    ; x = obj
    ; y = new handler entry (word access)

            lda ObjStateHI,x
            beq NullHandler                     ; don't handle anything with no entry

            sta Temp+1
            lda ObjStateLO,x
            sta Temp

            iny
            lda (Temp),y
            beq NullHandler                     ; no handler present for given event
            sta ObjFSMHI,x
            dey
            lda (Temp),y
            sta ObjFSMLO,x

   

ProcessFSM

    ; Vector to the creature's processing code
    ; x = creature

            lda ObjFSMLO,x
            sta Temp
            lda ObjFSMHI,x
            sta Temp+1
            jmp (Temp)

NullHandler rts




    ;------------------------------------------------------------------------------
    ; List of events

EVENT_DEFAULT           = 0                     ; default entry when switching states
EVENT_JOY_NULL          = 1
EVENT_JOY_UP            = 2
EVENT_JOY_DOWN          = 3
EVENT_JOY_LEFT          = 4
EVENT_JOY_RIGHT         = 5
EVENT_ATTACK_THROW      = 6

EVENT_INIT2             = 2


    ;------------------------------------------------------------------------------
    ; Automatically define states and a vector table to state-processing code
    ; This is fairly neat, as the ordering of the entries in the table auto-generates
    ; the appropriate equates to access the table correctly!

STATEQ      SET 0
            MAC STATENTRY
STATE_{1}   equ STATEQ
STATEQ      SET STATEQ + 1
            VECTOR State{1}
            ENDM

StateTables STATENTRY NORMAL

    ;------------------------------------------------------------------------------
    ; NORMAL state table
    ; Each State table is a table of pointers to code processing 'EVENTS'

StateNORMAL
            VECTOR NormalInit                ; 0     EVENT_DEFAULT
            VECTOR NormalWait                ; 1     EVENT_JOY_NULL
            VECTOR NormalInitRight           ; 2     EVENT_JOY_UP

    ;------------------------------------------------------------------------------
    ; NORMAL
    ; The basic default standing, doing nothing.


NormalInit  ANIMATION ANIMATION_STAND
            HANDLER EVENT_JOY_NULL
            rts

NormalWait  rts


NormalInitRight

            ANIMATION ANIMATION_STAND2
            HANDLER EVENT_JOY_NULL
            rts



; STATE Processing END
;------------------------------------------------------------------------------



VBProcessing

      
            ldx Player

            lda ObjXPosition,x
            sta DrawX
            lda #1
            sta DrawX+1
            lda ObjYPosition,x
            sta DrawY

            jsr ProcessFSM                  ; process creature FSM logic

            jsr AnimateObject               ; process object animation sequence
            jsr CalculateDrawPosition       ; setup position(s) for next VB draw

    ;------------------------------------------------------------------------


            ldy Player

            lda ObjFacing,y
            and #D7
            lsr
            lsr
            lsr
            lsr
            sta REFP0
            sta REFP1                   ;@17

            lda BGColour
            sta COLUBK

_RTS14      nop
            rts                         ; 14-cycle waste

    ;------------------------------------------------------------------------

NewFrame

    ; Start of vertical blank processing

            lda #$02
            sta WSYNC

            sta VBLANK          

            sta VSYNC           
            sta WSYNC           
            sta WSYNC
            sta WSYNC

            lda #$00
            sta VSYNC           

            lda #43             
            sta TIM64T

            lda #$00
            sta HMCLR

            jsr VBProcessing        ; spend 2000+ cycles

VblankLoop  lda INTIM
            bne VblankLoop      
            
            sta WSYNC           
            sta VBLANK          

    ;------------------------------------------------------------------------------
    ; START OF DISPLAY


            lda #238                ; NTSC
            sta TIM64T


    ;?
            lda     #%00010100      ; reflect, priority, 2 pixel wide ball
            sta     CTRLPF
    ;^?

            lda #PFCOL
            sta COLUPF
            
            lda #0
            sta PF0
            sta PF1
            sta PF2

            sta GRP0
            sta GRP1


    ;--------------------------------------------------------------------------
    ; Init the loop counters (16 rows each) for each of the rows

            lda #127
            sta LoopCount

            ldy Player
            lda ObjFrame,y
            bmi SkipDraw

  


            lda Player
            bne NotUP                   ; only roll the colours after both players done

            ldx Phase
            lda NextPhase,x
            sta Phase
   
NotUP       lda Phase
            asl
            tax
            lda PhasePtr,x
            sta RGBVec
            lda PhasePtr+1,x
            sta RGBVec+1

            jsr PositionObject
            jsr DrawSprite

            sta WSYNC
            
SkipDraw    lda #0
            sta GRP0
            sta GRP1
            sta GRP0            ; buffered??
            sta GRP1            ; buffered??

            sta VDELP0
            sta VDELP1

            sta REFP0
            sta REFP1

    ;--------------------------------------------------------------------------
    ; START OF COLOUR BITMAP DISPLAY KERNEL

            sta WSYNC

PadScreen2  lda INTIM
            bne PadScreen2
  
            sta HMCLR
            sta WSYNC

#if COLOUR = PAL

            lda #60
            sta TIM64T
PALTiming   lda INTIM
            bne PALTiming

#endif


            lda #D6+D1
            sta VBLANK                      ; end of screen - enter blanking

OverscanStart

            lda #25
            sta TIM64T

    ;--------------------------------------------------------------------------
    ; Switch to alternate player(s)
            
            dec Player
            bpl PlayerN
            lda #BIG_SPRITES-1
            sta Player
PlayerN


;            ldx PlayerN
;            ldy #EVENT_JOY_NULL*2
;            jsr SetHandler                  ; handle joystick event


Overscan    lda INTIM
            bne Overscan

            sta WSYNC           
            sta WSYNC           

            jmp NewFrame



    ;--------------------------------------------------------------------------

CalculateDrawPosition

    ; Given the current frame of the player, calculate a draw position such that
    ; the centerpoint is at the creature's (ObjXPosition,ObjYPosition) and that the
    ; left and right edges are then forced to be onscreen.

    ; Calculate the frame definition start address.  Each frame is a 8-byte
    ; definition block giving the bank containing the frame and a matrix of
    ; 128-sprite numbers making up the nx6 grid.

    ; FORMAT:
    ;    BYTE       centerpointx, centerpointy
    ;    BYTES...    0, 1, 2, 3, 4, 5   \ ;  1 x 6 matrix of 128-sprite #s

            ldy Player
  
            lda #0
            sta FrameAddress+1

            lda ObjFrame,y              ; animation frame (absolute)
            asl
            adc ObjFrame,y              ; Frametable is bank, AddressLO, AddressHI
            tax

            lda FrameTable+1,x
            sta FrameAddress
            lda FrameTable+2,x
            sta FrameAddress+1

            ldx #0
            lda ObjFacing,y
            bpl nMirror
            ldx #BIG_ROWS*BIG_COLS
nMirror


    ; Now we have a pointer to the frame definition block (FrameAddress)
    ; Go through the entire BIG_ROWS*BIG_COLS entries and convert the matrix 16-sprite
    ; number into an absolute address pointing to the sprite data.  This will correspond
    ; nicely to the vars used for the actual draw.

            ldy #0
            sty CenterX+1
            lda (FrameAddress),y
            sta CenterX
            iny
            lda (FrameAddress),y
            sta CenterY

            stx Temp+1

Mirrorable  iny

            inc Temp+1
            ldx Temp+1
            lda BaseMirror-1,x
            tax

            lda (FrameAddress),y

            lsr
            ora #$F0
            sta SPBASE+1,x
            lda #0
            ror
            sta SPBASE,x
            

            cpy #BIG_ROWS*BIG_COLS+1
            bcc Mirrorable


    ;--------------------------------------------------------------------------
    ; Centerpoint Adjustment based on frame

            ldy Player

            lda ObjFrame,y
            bmi SkipRepos

            lda ObjFacing,y
            bpl nM

            clc
            lda #0
            sbc CenterX
            sta CenterX
            lda #0
            sbc CenterX+1
            sta CenterX+1

            clc
            lda CenterX
            adc #48
            sta CenterX
            lda CenterX+1
            adc #0
            sta CenterX+1

nM

    ; Adjust draw position so that centerpoint is where the ObjXPosition is

            sec
            lda DrawX
            sbc CenterX
            sta VisualX
            lda DrawX+1
            sbc CenterX+1
            sta VisualX+1

            bne OKleft


    ; OK, so the object is offscreen (to the left)
    ; This means that, with the centerpoint adjustment, the left edge of the sprite is offscreen
    ; So we need to adjust the object position (DrawX,DrawY) such that the sprite will be onscreen
    ; As a minimum, we know we want the sprite to be at (0,DrawY).  So we just adjust the
    ; object position by the negative of the offsreen offset

            sec
            lda #0
            sbc VisualX                     ; all we really care about - the offset
            sta Temp
            adc DrawX                       ; adjust (what will be) the actual coordinate
            sta DrawX

    ; and set the visual draw position to left edge

            lda #0
            sta VisualX
            beq Onscreen

OKleft

    ; Check for right-hand side boundary conditions


            sec
            lda VisualX
            sbc #160-48
            sta Temp
            lda VisualX+1
            sbc #1
            bcc Onscreen

            lda Temp
            eor #$FF
            adc #0
            sta Temp

            adc DrawX
            sta DrawX


            lda #160-48
            sta VisualX

Onscreen    sec
            lda DrawY
            sbc CenterY
            sta VisualY
SkipRepos

    ;--------------------------------------------------------------------------

            ldx Player
            lda DrawX
            sta ObjXPosition,x
            lda DrawY
            sta ObjYPosition,x


            rts


    ;--------------------------------------------------------------------------

JNDelayDraw

            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c5

            nop
            nop
            nop
            nop

            nop
            nop
            nop
            nop
            nop
            nop

            rts

            ALIGN   256

JNDelayPos  
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9
            .byte   $c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c9,$c5

            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            nop
            cmp $80

            sta RESP0
            sta RESP1
            sta WSYNC
            sta HMOVE

            lda #<JNDelayDraw
            clc
            adc DelayTable,x
            sta Temp

            lda #>JNDelayDraw
            sta Temp+1

            sta WSYNC

            jmp (Temp)

MoveTable
            .byte   $30, $20

            REPEAT  37
                .byte   $40, $30, $20
            REPEND



            ALIGN 256
DelayTable
            .byte   37, 37
Q           SET     36
            REPEAT  37
            .byte   Q, Q, Q
Q           SET     Q-1
            REPEND



;--------------------------------------------------------------------------
; The beautiful, beautiful, draw loop which draws the entire matrix onscreen
; This caters for an adjustable (at compile-time) number of rows and also
; facilitates double-size pixels.

            SUBROUTINE

    ; Each sprite has 6 columns, each with a pointer to the column data
    ; setup in the vertical blank.  The columns are already mirrored (that
    ; is, they point to the correct column for the mirrored-state of the
    ; frame).  

.S1         SET SPBASE
.S2         SET SPBASE + 2
.S3         SET SPBASE + 4
.S4         SET SPBASE + 6
.S5         SET SPBASE + 8
.S6         SET SPBASE + 10

            ALIGN 256


    ; The following three sections (.PALG, .PALB, .PALR)
    ; *MUST NOT CROSS A PAGE BOUNDARY*


DrawSprite
            jmp (RGBVec)        ; Vector to the correct NTSC/SECAM/PAL *and*
                                ; Red/Green/Blue starting line.

    ;--------------------------------------------------------------------------
    ; Define the RGB component colours for all system variants (SECAM, NTSC, PAL)
    ; The ones actually USED are dependant on the value of COLOUR, which is
    ; set to either SECAM, NTSC, or PAL at the top. Don't touch any of this
    ; unless you specifically want to change the hue/intensity of the R/G/B
    ; component colour for a particular TV system.

SECAM_RED   = 4                 ; SECAM colours
SECAM_GREEN = 8
SECAM_BLUE  = 2

NTSC_RED    = $43                                 ;%00110100         ; NTSC colours
NTSC_GREEN  = $C6                                 ;%11000110
NTSC_BLUE   = $74                          ;%01110100

PAL_RED     = $64               ; PAL colours
PAL_GREEN   = $54
PAL_BLUE    = $D4

#if COLOUR = SECAM
RED         = SECAM_RED
GREEN       = SECAM_GREEN
BLUE        = SECAM_BLUE
#endif

#if COLOUR = NTSC
RED         = NTSC_RED
GREEN       = NTSC_GREEN
BLUE        = NTSC_BLUE
#endif

#if COLOUR = PAL
RED         = PAL_RED
GREEN       = PAL_GREEN
BLUE        = PAL_BLUE
#endif

    ;--------------------------------------------------------------------------
    ; Each section (eg: .LABG) draws a single-line in the appropriate colour
    ; (in this case, green) and then decrements the line-counter.  If there's
    ; another line, then the immediate next-colour (eg: RED) is drawn, then
    ; the next, etc.  Code is exquisitely timed so that each line takes 
    ; *EXACTLY* 76 cycles.  Code cannot cross page-boundaries, as the branch
    ; would then take an extra cycle, and bugger the display.

.LABG       lda #GREEN          ; 2
            sta COLUP0          ; 3
            sta COLUP1          ; 3

            ldy LoopCount       ; 3

            lda (.S1),y         ; 5
            sta GRP0            ; 3
            lda (.S2),y         ; 5
            sta GRP1            ; 3
            lda (.S3),y         ; 5
            sta GRP0            ; 3

            lda (.S6),y         ; 5
            sta Temp            ; 3
            .byte $b3,.S5       ; 5  --> lax (.S5),y
            lda (.S4),y         ; 5
            ldy Temp            ; 3
            sta GRP1            ; 3
            stx GRP0            ; 3
            sty GRP1            ; 3
            sta GRP0            ; 3
            
            dec LoopCount       ; 5
            bpl .LABB           ; 3
    
            bmi EndDraw

.LABR       lda #RED            ; 2
            sta COLUP0          ; 3
            sta COLUP1          ; 3

            ldy LoopCount       ; 3

            lda (.S1),y         ; 5
            sta GRP0            ; 3
            lda (.S2),y         ; 5
            sta GRP1            ; 3
            lda (.S3),y         ; 5
            sta GRP0            ; 3

            lda (.S6),y         ; 5
            sta Temp            ; 3
            .byte $b3,.S5       ; 5  --> lax (.S5),y
            lda (.S4),y         ; 5
            ldy Temp            ; 3
            sta GRP1            ; 3
            stx GRP0            ; 3
            sty GRP1            ; 3
            sta GRP0            ; 3
            
            dec LoopCount       ; 5
            bpl .LABG           ; 3

            bmi EndDraw

.LABB       lda #BLUE           ; 2
            sta COLUP0          ; 3
            sta COLUP1          ; 3

            ldy LoopCount       ; 3

            lda (.S1),y         ; 5
            sta GRP0            ; 3
            lda (.S2),y         ; 5
            sta GRP1            ; 3
            lda (.S3),y         ; 5
            sta GRP0            ; 3

            lda (.S6),y         ; 5
            sta Temp            ; 3
            .byte $b3,.S5       ; 5  --> lax (.S5),y
            lda (.S4),y         ; 5
            ldy Temp            ; 3
            sta GRP1            ; 3
            stx GRP0            ; 3
            sty GRP1            ; 3
            sta GRP0            ; 3
            
            dec LoopCount       ; 5
            bpl .LABR           ; 3

EndDraw     rts


    ;--------------------------------------------------------------------------
    ; Object X,Y positioning
    ; Timing is absolutely critical here!

PositionObject
    ; Waste scanlines to start of object position, giving our vertical movement
            
            lda #0
            sta PF2

            ldx VisualY
            inx
DelayVert   sta WSYNC
            dex
            bne DelayVert

    ; Now the horizontal magic (which isn't working (1/MAR))

            sta WSYNC

            ldx VisualX
            clc
            lda MoveTable,x
            sta HMP0
            adc #$10
            sta HMP1

            lda #1
            sta VDELP0
            sta VDELP1

            lda #3
            sta NUSIZ0
            sta NUSIZ1

            clc
            lda #<JNDelayPos
            adc DelayTable,x
            sta Temp
            lda #>JNDelayPos
;            adc #0
            sta Temp+1

            jmp (Temp)


    ;--------------------------------------------------------------------------
    ; Table allows the sprite system to mirror.  It effectively swaps what
    ; sprite shape pointer is used for each sprite column.  Sprite setup is
    ; done in the vertical blank.

BaseMirror

.SP         SET 0
            REPEAT BIG_ROWS*BIG_COLS
            .byte .SP
.SP         SET .SP + 2
            REPEND
.SPBASE     SET 0
            REPEAT BIG_ROWS
.SPOFF      SET 10
            REPEAT BIG_COLS
            .byte .SPBASE + .SPOFF
.SPOFF      SET .SPOFF-2
            REPEND
.SPBASE     SET .SPBASE + 12
            REPEND

    ;--------------------------------------------------------------------------
    ; Table rolls the RGB on a per-line basis, giving the next index to the
    ; PhasePtr table, given the current index.  ie: next(0) = 1,   next(2) = 0

NextPhase   .byte 1,2,0

    ;--------------------------------------------------------------------------
    ; Table vectors to the correct START line/colour.  The lines themselves
    ; move along to the next line colour automatically.  That is, RED will
    ; vector to GREEN, etc.

PhasePtr    .word .LABR,.LABG,.LABB

    ;--------------------------------------------------------------------------

            ORG $Fffa   ;IntVectors

            VECTOR Reset           ; NMI        ( not really needed )
            VECTOR Reset           ; RESET
            VECTOR Reset           ; IRQ

    		END

