; Atari 2600 Image Optimizer: 96-pixel interleaved bitmap; NTSC / 32K F4
; Each visible row is unrolled. No data-dependent branches in the raster.
 processor 6502
 SEG
 ORG $0000
 RORG $F000
 sta $02
P_0_0 = *+1
 lda #$00
 sta $09
P_0_1 = *+1
 lda #$00
 sta $06
P_0_2 = *+1
 lda #$00
 sta $07
P_0_3 = *+1
 lda #$00
 sta $1B
P_0_4 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_5 = *+1
 lda #$00
 sta $1B
P_0_6 = *+1
 lda #$00
 sta $1C
P_0_7 = *+1
 lda #$00
 sta $1B
P_0_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_9 = *+1
 lda #$00
 sta $09
P_0_10 = *+1
 lda #$00
 sta $06
P_0_11 = *+1
 lda #$00
 sta $07
P_0_12 = *+1
 lda #$00
 sta $1B
P_0_13 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_14 = *+1
 lda #$00
 sta $1B
P_0_15 = *+1
 lda #$00
 sta $1C
P_0_16 = *+1
 lda #$00
 sta $1B
P_0_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_18 = *+1
 lda #$00
 sta $09
P_0_19 = *+1
 lda #$00
 sta $06
P_0_20 = *+1
 lda #$00
 sta $07
P_0_21 = *+1
 lda #$00
 sta $1B
P_0_22 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_23 = *+1
 lda #$00
 sta $1B
P_0_24 = *+1
 lda #$00
 sta $1C
P_0_25 = *+1
 lda #$00
 sta $1B
P_0_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_27 = *+1
 lda #$00
 sta $09
P_0_28 = *+1
 lda #$00
 sta $06
P_0_29 = *+1
 lda #$00
 sta $07
P_0_30 = *+1
 lda #$00
 sta $1B
P_0_31 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_32 = *+1
 lda #$00
 sta $1B
P_0_33 = *+1
 lda #$00
 sta $1C
P_0_34 = *+1
 lda #$00
 sta $1B
P_0_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_36 = *+1
 lda #$00
 sta $09
P_0_37 = *+1
 lda #$00
 sta $06
P_0_38 = *+1
 lda #$00
 sta $07
P_0_39 = *+1
 lda #$00
 sta $1B
P_0_40 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_41 = *+1
 lda #$00
 sta $1B
P_0_42 = *+1
 lda #$00
 sta $1C
P_0_43 = *+1
 lda #$00
 sta $1B
P_0_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_45 = *+1
 lda #$00
 sta $09
P_0_46 = *+1
 lda #$00
 sta $06
P_0_47 = *+1
 lda #$00
 sta $07
P_0_48 = *+1
 lda #$00
 sta $1B
P_0_49 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_50 = *+1
 lda #$00
 sta $1B
P_0_51 = *+1
 lda #$00
 sta $1C
P_0_52 = *+1
 lda #$00
 sta $1B
P_0_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_54 = *+1
 lda #$00
 sta $09
P_0_55 = *+1
 lda #$00
 sta $06
P_0_56 = *+1
 lda #$00
 sta $07
P_0_57 = *+1
 lda #$00
 sta $1B
P_0_58 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_59 = *+1
 lda #$00
 sta $1B
P_0_60 = *+1
 lda #$00
 sta $1C
P_0_61 = *+1
 lda #$00
 sta $1B
P_0_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_63 = *+1
 lda #$00
 sta $09
P_0_64 = *+1
 lda #$00
 sta $06
P_0_65 = *+1
 lda #$00
 sta $07
P_0_66 = *+1
 lda #$00
 sta $1B
P_0_67 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_68 = *+1
 lda #$00
 sta $1B
P_0_69 = *+1
 lda #$00
 sta $1C
P_0_70 = *+1
 lda #$00
 sta $1B
P_0_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_72 = *+1
 lda #$00
 sta $09
P_0_73 = *+1
 lda #$00
 sta $06
P_0_74 = *+1
 lda #$00
 sta $07
P_0_75 = *+1
 lda #$00
 sta $1B
P_0_76 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_77 = *+1
 lda #$00
 sta $1B
P_0_78 = *+1
 lda #$00
 sta $1C
P_0_79 = *+1
 lda #$00
 sta $1B
P_0_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_81 = *+1
 lda #$00
 sta $09
P_0_82 = *+1
 lda #$00
 sta $06
P_0_83 = *+1
 lda #$00
 sta $07
P_0_84 = *+1
 lda #$00
 sta $1B
P_0_85 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_86 = *+1
 lda #$00
 sta $1B
P_0_87 = *+1
 lda #$00
 sta $1C
P_0_88 = *+1
 lda #$00
 sta $1B
P_0_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_90 = *+1
 lda #$00
 sta $09
P_0_91 = *+1
 lda #$00
 sta $06
P_0_92 = *+1
 lda #$00
 sta $07
P_0_93 = *+1
 lda #$00
 sta $1B
P_0_94 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_95 = *+1
 lda #$00
 sta $1B
P_0_96 = *+1
 lda #$00
 sta $1C
P_0_97 = *+1
 lda #$00
 sta $1B
P_0_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_99 = *+1
 lda #$00
 sta $09
P_0_100 = *+1
 lda #$00
 sta $06
P_0_101 = *+1
 lda #$00
 sta $07
P_0_102 = *+1
 lda #$00
 sta $1B
P_0_103 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_104 = *+1
 lda #$00
 sta $1B
P_0_105 = *+1
 lda #$00
 sta $1C
P_0_106 = *+1
 lda #$00
 sta $1B
P_0_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_108 = *+1
 lda #$00
 sta $09
P_0_109 = *+1
 lda #$00
 sta $06
P_0_110 = *+1
 lda #$00
 sta $07
P_0_111 = *+1
 lda #$00
 sta $1B
P_0_112 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_113 = *+1
 lda #$00
 sta $1B
P_0_114 = *+1
 lda #$00
 sta $1C
P_0_115 = *+1
 lda #$00
 sta $1B
P_0_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_117 = *+1
 lda #$00
 sta $09
P_0_118 = *+1
 lda #$00
 sta $06
P_0_119 = *+1
 lda #$00
 sta $07
P_0_120 = *+1
 lda #$00
 sta $1B
P_0_121 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_122 = *+1
 lda #$00
 sta $1B
P_0_123 = *+1
 lda #$00
 sta $1C
P_0_124 = *+1
 lda #$00
 sta $1B
P_0_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_126 = *+1
 lda #$00
 sta $09
P_0_127 = *+1
 lda #$00
 sta $06
P_0_128 = *+1
 lda #$00
 sta $07
P_0_129 = *+1
 lda #$00
 sta $1B
P_0_130 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_131 = *+1
 lda #$00
 sta $1B
P_0_132 = *+1
 lda #$00
 sta $1C
P_0_133 = *+1
 lda #$00
 sta $1B
P_0_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_135 = *+1
 lda #$00
 sta $09
P_0_136 = *+1
 lda #$00
 sta $06
P_0_137 = *+1
 lda #$00
 sta $07
P_0_138 = *+1
 lda #$00
 sta $1B
P_0_139 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_140 = *+1
 lda #$00
 sta $1B
P_0_141 = *+1
 lda #$00
 sta $1C
P_0_142 = *+1
 lda #$00
 sta $1B
P_0_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_144 = *+1
 lda #$00
 sta $09
P_0_145 = *+1
 lda #$00
 sta $06
P_0_146 = *+1
 lda #$00
 sta $07
P_0_147 = *+1
 lda #$00
 sta $1B
P_0_148 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_149 = *+1
 lda #$00
 sta $1B
P_0_150 = *+1
 lda #$00
 sta $1C
P_0_151 = *+1
 lda #$00
 sta $1B
P_0_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_153 = *+1
 lda #$00
 sta $09
P_0_154 = *+1
 lda #$00
 sta $06
P_0_155 = *+1
 lda #$00
 sta $07
P_0_156 = *+1
 lda #$00
 sta $1B
P_0_157 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_158 = *+1
 lda #$00
 sta $1B
P_0_159 = *+1
 lda #$00
 sta $1C
P_0_160 = *+1
 lda #$00
 sta $1B
P_0_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_162 = *+1
 lda #$00
 sta $09
P_0_163 = *+1
 lda #$00
 sta $06
P_0_164 = *+1
 lda #$00
 sta $07
P_0_165 = *+1
 lda #$00
 sta $1B
P_0_166 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_167 = *+1
 lda #$00
 sta $1B
P_0_168 = *+1
 lda #$00
 sta $1C
P_0_169 = *+1
 lda #$00
 sta $1B
P_0_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_171 = *+1
 lda #$00
 sta $09
P_0_172 = *+1
 lda #$00
 sta $06
P_0_173 = *+1
 lda #$00
 sta $07
P_0_174 = *+1
 lda #$00
 sta $1B
P_0_175 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_176 = *+1
 lda #$00
 sta $1B
P_0_177 = *+1
 lda #$00
 sta $1C
P_0_178 = *+1
 lda #$00
 sta $1B
P_0_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_180 = *+1
 lda #$00
 sta $09
P_0_181 = *+1
 lda #$00
 sta $06
P_0_182 = *+1
 lda #$00
 sta $07
P_0_183 = *+1
 lda #$00
 sta $1B
P_0_184 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_185 = *+1
 lda #$00
 sta $1B
P_0_186 = *+1
 lda #$00
 sta $1C
P_0_187 = *+1
 lda #$00
 sta $1B
P_0_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_189 = *+1
 lda #$00
 sta $09
P_0_190 = *+1
 lda #$00
 sta $06
P_0_191 = *+1
 lda #$00
 sta $07
P_0_192 = *+1
 lda #$00
 sta $1B
P_0_193 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_194 = *+1
 lda #$00
 sta $1B
P_0_195 = *+1
 lda #$00
 sta $1C
P_0_196 = *+1
 lda #$00
 sta $1B
P_0_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_198 = *+1
 lda #$00
 sta $09
P_0_199 = *+1
 lda #$00
 sta $06
P_0_200 = *+1
 lda #$00
 sta $07
P_0_201 = *+1
 lda #$00
 sta $1B
P_0_202 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_203 = *+1
 lda #$00
 sta $1B
P_0_204 = *+1
 lda #$00
 sta $1C
P_0_205 = *+1
 lda #$00
 sta $1B
P_0_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_207 = *+1
 lda #$00
 sta $09
P_0_208 = *+1
 lda #$00
 sta $06
P_0_209 = *+1
 lda #$00
 sta $07
P_0_210 = *+1
 lda #$00
 sta $1B
P_0_211 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_212 = *+1
 lda #$00
 sta $1B
P_0_213 = *+1
 lda #$00
 sta $1C
P_0_214 = *+1
 lda #$00
 sta $1B
P_0_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_216 = *+1
 lda #$00
 sta $09
P_0_217 = *+1
 lda #$00
 sta $06
P_0_218 = *+1
 lda #$00
 sta $07
P_0_219 = *+1
 lda #$00
 sta $1B
P_0_220 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_221 = *+1
 lda #$00
 sta $1B
P_0_222 = *+1
 lda #$00
 sta $1C
P_0_223 = *+1
 lda #$00
 sta $1B
P_0_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_225 = *+1
 lda #$00
 sta $09
P_0_226 = *+1
 lda #$00
 sta $06
P_0_227 = *+1
 lda #$00
 sta $07
P_0_228 = *+1
 lda #$00
 sta $1B
P_0_229 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_230 = *+1
 lda #$00
 sta $1B
P_0_231 = *+1
 lda #$00
 sta $1C
P_0_232 = *+1
 lda #$00
 sta $1B
P_0_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_234 = *+1
 lda #$00
 sta $09
P_0_235 = *+1
 lda #$00
 sta $06
P_0_236 = *+1
 lda #$00
 sta $07
P_0_237 = *+1
 lda #$00
 sta $1B
P_0_238 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_239 = *+1
 lda #$00
 sta $1B
P_0_240 = *+1
 lda #$00
 sta $1C
P_0_241 = *+1
 lda #$00
 sta $1B
P_0_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_243 = *+1
 lda #$00
 sta $09
P_0_244 = *+1
 lda #$00
 sta $06
P_0_245 = *+1
 lda #$00
 sta $07
P_0_246 = *+1
 lda #$00
 sta $1B
P_0_247 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_248 = *+1
 lda #$00
 sta $1B
P_0_249 = *+1
 lda #$00
 sta $1C
P_0_250 = *+1
 lda #$00
 sta $1B
P_0_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_252 = *+1
 lda #$00
 sta $09
P_0_253 = *+1
 lda #$00
 sta $06
P_0_254 = *+1
 lda #$00
 sta $07
P_0_255 = *+1
 lda #$00
 sta $1B
P_0_256 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_257 = *+1
 lda #$00
 sta $1B
P_0_258 = *+1
 lda #$00
 sta $1C
P_0_259 = *+1
 lda #$00
 sta $1B
P_0_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_261 = *+1
 lda #$00
 sta $09
P_0_262 = *+1
 lda #$00
 sta $06
P_0_263 = *+1
 lda #$00
 sta $07
P_0_264 = *+1
 lda #$00
 sta $1B
P_0_265 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_266 = *+1
 lda #$00
 sta $1B
P_0_267 = *+1
 lda #$00
 sta $1C
P_0_268 = *+1
 lda #$00
 sta $1B
P_0_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_270 = *+1
 lda #$00
 sta $09
P_0_271 = *+1
 lda #$00
 sta $06
P_0_272 = *+1
 lda #$00
 sta $07
P_0_273 = *+1
 lda #$00
 sta $1B
P_0_274 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_275 = *+1
 lda #$00
 sta $1B
P_0_276 = *+1
 lda #$00
 sta $1C
P_0_277 = *+1
 lda #$00
 sta $1B
P_0_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_279 = *+1
 lda #$00
 sta $09
P_0_280 = *+1
 lda #$00
 sta $06
P_0_281 = *+1
 lda #$00
 sta $07
P_0_282 = *+1
 lda #$00
 sta $1B
P_0_283 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_284 = *+1
 lda #$00
 sta $1B
P_0_285 = *+1
 lda #$00
 sta $1C
P_0_286 = *+1
 lda #$00
 sta $1B
P_0_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_288 = *+1
 lda #$00
 sta $09
P_0_289 = *+1
 lda #$00
 sta $06
P_0_290 = *+1
 lda #$00
 sta $07
P_0_291 = *+1
 lda #$00
 sta $1B
P_0_292 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_293 = *+1
 lda #$00
 sta $1B
P_0_294 = *+1
 lda #$00
 sta $1C
P_0_295 = *+1
 lda #$00
 sta $1B
P_0_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_297 = *+1
 lda #$00
 sta $09
P_0_298 = *+1
 lda #$00
 sta $06
P_0_299 = *+1
 lda #$00
 sta $07
P_0_300 = *+1
 lda #$00
 sta $1B
P_0_301 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_302 = *+1
 lda #$00
 sta $1B
P_0_303 = *+1
 lda #$00
 sta $1C
P_0_304 = *+1
 lda #$00
 sta $1B
P_0_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_306 = *+1
 lda #$00
 sta $09
P_0_307 = *+1
 lda #$00
 sta $06
P_0_308 = *+1
 lda #$00
 sta $07
P_0_309 = *+1
 lda #$00
 sta $1B
P_0_310 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_311 = *+1
 lda #$00
 sta $1B
P_0_312 = *+1
 lda #$00
 sta $1C
P_0_313 = *+1
 lda #$00
 sta $1B
P_0_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_315 = *+1
 lda #$00
 sta $09
P_0_316 = *+1
 lda #$00
 sta $06
P_0_317 = *+1
 lda #$00
 sta $07
P_0_318 = *+1
 lda #$00
 sta $1B
P_0_319 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_320 = *+1
 lda #$00
 sta $1B
P_0_321 = *+1
 lda #$00
 sta $1C
P_0_322 = *+1
 lda #$00
 sta $1B
P_0_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_324 = *+1
 lda #$00
 sta $09
P_0_325 = *+1
 lda #$00
 sta $06
P_0_326 = *+1
 lda #$00
 sta $07
P_0_327 = *+1
 lda #$00
 sta $1B
P_0_328 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_329 = *+1
 lda #$00
 sta $1B
P_0_330 = *+1
 lda #$00
 sta $1C
P_0_331 = *+1
 lda #$00
 sta $1B
P_0_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_333 = *+1
 lda #$00
 sta $09
P_0_334 = *+1
 lda #$00
 sta $06
P_0_335 = *+1
 lda #$00
 sta $07
P_0_336 = *+1
 lda #$00
 sta $1B
P_0_337 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_338 = *+1
 lda #$00
 sta $1B
P_0_339 = *+1
 lda #$00
 sta $1C
P_0_340 = *+1
 lda #$00
 sta $1B
P_0_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_342 = *+1
 lda #$00
 sta $09
P_0_343 = *+1
 lda #$00
 sta $06
P_0_344 = *+1
 lda #$00
 sta $07
P_0_345 = *+1
 lda #$00
 sta $1B
P_0_346 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_347 = *+1
 lda #$00
 sta $1B
P_0_348 = *+1
 lda #$00
 sta $1C
P_0_349 = *+1
 lda #$00
 sta $1B
P_0_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_351 = *+1
 lda #$00
 sta $09
P_0_352 = *+1
 lda #$00
 sta $06
P_0_353 = *+1
 lda #$00
 sta $07
P_0_354 = *+1
 lda #$00
 sta $1B
P_0_355 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_356 = *+1
 lda #$00
 sta $1B
P_0_357 = *+1
 lda #$00
 sta $1C
P_0_358 = *+1
 lda #$00
 sta $1B
P_0_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_360 = *+1
 lda #$00
 sta $09
P_0_361 = *+1
 lda #$00
 sta $06
P_0_362 = *+1
 lda #$00
 sta $07
P_0_363 = *+1
 lda #$00
 sta $1B
P_0_364 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_365 = *+1
 lda #$00
 sta $1B
P_0_366 = *+1
 lda #$00
 sta $1C
P_0_367 = *+1
 lda #$00
 sta $1B
P_0_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_369 = *+1
 lda #$00
 sta $09
P_0_370 = *+1
 lda #$00
 sta $06
P_0_371 = *+1
 lda #$00
 sta $07
P_0_372 = *+1
 lda #$00
 sta $1B
P_0_373 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_374 = *+1
 lda #$00
 sta $1B
P_0_375 = *+1
 lda #$00
 sta $1C
P_0_376 = *+1
 lda #$00
 sta $1B
P_0_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_378 = *+1
 lda #$00
 sta $09
P_0_379 = *+1
 lda #$00
 sta $06
P_0_380 = *+1
 lda #$00
 sta $07
P_0_381 = *+1
 lda #$00
 sta $1B
P_0_382 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_383 = *+1
 lda #$00
 sta $1B
P_0_384 = *+1
 lda #$00
 sta $1C
P_0_385 = *+1
 lda #$00
 sta $1B
P_0_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_387 = *+1
 lda #$00
 sta $09
P_0_388 = *+1
 lda #$00
 sta $06
P_0_389 = *+1
 lda #$00
 sta $07
P_0_390 = *+1
 lda #$00
 sta $1B
P_0_391 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_392 = *+1
 lda #$00
 sta $1B
P_0_393 = *+1
 lda #$00
 sta $1C
P_0_394 = *+1
 lda #$00
 sta $1B
P_0_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_396 = *+1
 lda #$00
 sta $09
P_0_397 = *+1
 lda #$00
 sta $06
P_0_398 = *+1
 lda #$00
 sta $07
P_0_399 = *+1
 lda #$00
 sta $1B
P_0_400 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_401 = *+1
 lda #$00
 sta $1B
P_0_402 = *+1
 lda #$00
 sta $1C
P_0_403 = *+1
 lda #$00
 sta $1B
P_0_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_405 = *+1
 lda #$00
 sta $09
P_0_406 = *+1
 lda #$00
 sta $06
P_0_407 = *+1
 lda #$00
 sta $07
P_0_408 = *+1
 lda #$00
 sta $1B
P_0_409 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_410 = *+1
 lda #$00
 sta $1B
P_0_411 = *+1
 lda #$00
 sta $1C
P_0_412 = *+1
 lda #$00
 sta $1B
P_0_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_414 = *+1
 lda #$00
 sta $09
P_0_415 = *+1
 lda #$00
 sta $06
P_0_416 = *+1
 lda #$00
 sta $07
P_0_417 = *+1
 lda #$00
 sta $1B
P_0_418 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_419 = *+1
 lda #$00
 sta $1B
P_0_420 = *+1
 lda #$00
 sta $1C
P_0_421 = *+1
 lda #$00
 sta $1B
P_0_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_423 = *+1
 lda #$00
 sta $09
P_0_424 = *+1
 lda #$00
 sta $06
P_0_425 = *+1
 lda #$00
 sta $07
P_0_426 = *+1
 lda #$00
 sta $1B
P_0_427 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_428 = *+1
 lda #$00
 sta $1B
P_0_429 = *+1
 lda #$00
 sta $1C
P_0_430 = *+1
 lda #$00
 sta $1B
P_0_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_432 = *+1
 lda #$00
 sta $09
P_0_433 = *+1
 lda #$00
 sta $06
P_0_434 = *+1
 lda #$00
 sta $07
P_0_435 = *+1
 lda #$00
 sta $1B
P_0_436 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_437 = *+1
 lda #$00
 sta $1B
P_0_438 = *+1
 lda #$00
 sta $1C
P_0_439 = *+1
 lda #$00
 sta $1B
P_0_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_441 = *+1
 lda #$00
 sta $09
P_0_442 = *+1
 lda #$00
 sta $06
P_0_443 = *+1
 lda #$00
 sta $07
P_0_444 = *+1
 lda #$00
 sta $1B
P_0_445 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_446 = *+1
 lda #$00
 sta $1B
P_0_447 = *+1
 lda #$00
 sta $1C
P_0_448 = *+1
 lda #$00
 sta $1B
P_0_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_450 = *+1
 lda #$00
 sta $09
P_0_451 = *+1
 lda #$00
 sta $06
P_0_452 = *+1
 lda #$00
 sta $07
P_0_453 = *+1
 lda #$00
 sta $1B
P_0_454 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_455 = *+1
 lda #$00
 sta $1B
P_0_456 = *+1
 lda #$00
 sta $1C
P_0_457 = *+1
 lda #$00
 sta $1B
P_0_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_459 = *+1
 lda #$00
 sta $09
P_0_460 = *+1
 lda #$00
 sta $06
P_0_461 = *+1
 lda #$00
 sta $07
P_0_462 = *+1
 lda #$00
 sta $1B
P_0_463 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_464 = *+1
 lda #$00
 sta $1B
P_0_465 = *+1
 lda #$00
 sta $1C
P_0_466 = *+1
 lda #$00
 sta $1B
P_0_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_468 = *+1
 lda #$00
 sta $09
P_0_469 = *+1
 lda #$00
 sta $06
P_0_470 = *+1
 lda #$00
 sta $07
P_0_471 = *+1
 lda #$00
 sta $1B
P_0_472 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_473 = *+1
 lda #$00
 sta $1B
P_0_474 = *+1
 lda #$00
 sta $1C
P_0_475 = *+1
 lda #$00
 sta $1B
P_0_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_477 = *+1
 lda #$00
 sta $09
P_0_478 = *+1
 lda #$00
 sta $06
P_0_479 = *+1
 lda #$00
 sta $07
P_0_480 = *+1
 lda #$00
 sta $1B
P_0_481 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_482 = *+1
 lda #$00
 sta $1B
P_0_483 = *+1
 lda #$00
 sta $1C
P_0_484 = *+1
 lda #$00
 sta $1B
P_0_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_486 = *+1
 lda #$00
 sta $09
P_0_487 = *+1
 lda #$00
 sta $06
P_0_488 = *+1
 lda #$00
 sta $07
P_0_489 = *+1
 lda #$00
 sta $1B
P_0_490 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_491 = *+1
 lda #$00
 sta $1B
P_0_492 = *+1
 lda #$00
 sta $1C
P_0_493 = *+1
 lda #$00
 sta $1B
P_0_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_495 = *+1
 lda #$00
 sta $09
P_0_496 = *+1
 lda #$00
 sta $06
P_0_497 = *+1
 lda #$00
 sta $07
P_0_498 = *+1
 lda #$00
 sta $1B
P_0_499 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_500 = *+1
 lda #$00
 sta $1B
P_0_501 = *+1
 lda #$00
 sta $1C
P_0_502 = *+1
 lda #$00
 sta $1B
P_0_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_504 = *+1
 lda #$00
 sta $09
P_0_505 = *+1
 lda #$00
 sta $06
P_0_506 = *+1
 lda #$00
 sta $07
P_0_507 = *+1
 lda #$00
 sta $1B
P_0_508 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_509 = *+1
 lda #$00
 sta $1B
P_0_510 = *+1
 lda #$00
 sta $1C
P_0_511 = *+1
 lda #$00
 sta $1B
P_0_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_513 = *+1
 lda #$00
 sta $09
P_0_514 = *+1
 lda #$00
 sta $06
P_0_515 = *+1
 lda #$00
 sta $07
P_0_516 = *+1
 lda #$00
 sta $1B
P_0_517 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_518 = *+1
 lda #$00
 sta $1B
P_0_519 = *+1
 lda #$00
 sta $1C
P_0_520 = *+1
 lda #$00
 sta $1B
P_0_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_522 = *+1
 lda #$00
 sta $09
P_0_523 = *+1
 lda #$00
 sta $06
P_0_524 = *+1
 lda #$00
 sta $07
P_0_525 = *+1
 lda #$00
 sta $1B
P_0_526 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_527 = *+1
 lda #$00
 sta $1B
P_0_528 = *+1
 lda #$00
 sta $1C
P_0_529 = *+1
 lda #$00
 sta $1B
P_0_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_531 = *+1
 lda #$00
 sta $09
P_0_532 = *+1
 lda #$00
 sta $06
P_0_533 = *+1
 lda #$00
 sta $07
P_0_534 = *+1
 lda #$00
 sta $1B
P_0_535 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_536 = *+1
 lda #$00
 sta $1B
P_0_537 = *+1
 lda #$00
 sta $1C
P_0_538 = *+1
 lda #$00
 sta $1B
P_0_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_540 = *+1
 lda #$00
 sta $09
P_0_541 = *+1
 lda #$00
 sta $06
P_0_542 = *+1
 lda #$00
 sta $07
P_0_543 = *+1
 lda #$00
 sta $1B
P_0_544 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_545 = *+1
 lda #$00
 sta $1B
P_0_546 = *+1
 lda #$00
 sta $1C
P_0_547 = *+1
 lda #$00
 sta $1B
P_0_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_549 = *+1
 lda #$00
 sta $09
P_0_550 = *+1
 lda #$00
 sta $06
P_0_551 = *+1
 lda #$00
 sta $07
P_0_552 = *+1
 lda #$00
 sta $1B
P_0_553 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_554 = *+1
 lda #$00
 sta $1B
P_0_555 = *+1
 lda #$00
 sta $1C
P_0_556 = *+1
 lda #$00
 sta $1B
P_0_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_558 = *+1
 lda #$00
 sta $09
P_0_559 = *+1
 lda #$00
 sta $06
P_0_560 = *+1
 lda #$00
 sta $07
P_0_561 = *+1
 lda #$00
 sta $1B
P_0_562 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_563 = *+1
 lda #$00
 sta $1B
P_0_564 = *+1
 lda #$00
 sta $1C
P_0_565 = *+1
 lda #$00
 sta $1B
P_0_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_0_567 = *+1
 lda #$00
 sta $09
P_0_568 = *+1
 lda #$00
 sta $06
P_0_569 = *+1
 lda #$00
 sta $07
P_0_570 = *+1
 lda #$00
 sta $1B
P_0_571 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_0_572 = *+1
 lda #$00
 sta $1B
P_0_573 = *+1
 lda #$00
 sta $1C
P_0_574 = *+1
 lda #$00
 sta $1B
P_0_575 = *+1
 lda #$00
 sta $1C
 jmp $FF00
 ORG $0F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $0FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $1000
 RORG $F000
 sta $02
P_1_0 = *+1
 lda #$00
 sta $09
P_1_1 = *+1
 lda #$00
 sta $06
P_1_2 = *+1
 lda #$00
 sta $07
P_1_3 = *+1
 lda #$00
 sta $1B
P_1_4 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_5 = *+1
 lda #$00
 sta $1B
P_1_6 = *+1
 lda #$00
 sta $1C
P_1_7 = *+1
 lda #$00
 sta $1B
P_1_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_9 = *+1
 lda #$00
 sta $09
P_1_10 = *+1
 lda #$00
 sta $06
P_1_11 = *+1
 lda #$00
 sta $07
P_1_12 = *+1
 lda #$00
 sta $1B
P_1_13 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_14 = *+1
 lda #$00
 sta $1B
P_1_15 = *+1
 lda #$00
 sta $1C
P_1_16 = *+1
 lda #$00
 sta $1B
P_1_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_18 = *+1
 lda #$00
 sta $09
P_1_19 = *+1
 lda #$00
 sta $06
P_1_20 = *+1
 lda #$00
 sta $07
P_1_21 = *+1
 lda #$00
 sta $1B
P_1_22 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_23 = *+1
 lda #$00
 sta $1B
P_1_24 = *+1
 lda #$00
 sta $1C
P_1_25 = *+1
 lda #$00
 sta $1B
P_1_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_27 = *+1
 lda #$00
 sta $09
P_1_28 = *+1
 lda #$00
 sta $06
P_1_29 = *+1
 lda #$00
 sta $07
P_1_30 = *+1
 lda #$00
 sta $1B
P_1_31 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_32 = *+1
 lda #$00
 sta $1B
P_1_33 = *+1
 lda #$00
 sta $1C
P_1_34 = *+1
 lda #$00
 sta $1B
P_1_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_36 = *+1
 lda #$00
 sta $09
P_1_37 = *+1
 lda #$00
 sta $06
P_1_38 = *+1
 lda #$00
 sta $07
P_1_39 = *+1
 lda #$00
 sta $1B
P_1_40 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_41 = *+1
 lda #$00
 sta $1B
P_1_42 = *+1
 lda #$00
 sta $1C
P_1_43 = *+1
 lda #$00
 sta $1B
P_1_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_45 = *+1
 lda #$00
 sta $09
P_1_46 = *+1
 lda #$00
 sta $06
P_1_47 = *+1
 lda #$00
 sta $07
P_1_48 = *+1
 lda #$00
 sta $1B
P_1_49 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_50 = *+1
 lda #$00
 sta $1B
P_1_51 = *+1
 lda #$00
 sta $1C
P_1_52 = *+1
 lda #$00
 sta $1B
P_1_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_54 = *+1
 lda #$00
 sta $09
P_1_55 = *+1
 lda #$00
 sta $06
P_1_56 = *+1
 lda #$00
 sta $07
P_1_57 = *+1
 lda #$00
 sta $1B
P_1_58 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_59 = *+1
 lda #$00
 sta $1B
P_1_60 = *+1
 lda #$00
 sta $1C
P_1_61 = *+1
 lda #$00
 sta $1B
P_1_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_63 = *+1
 lda #$00
 sta $09
P_1_64 = *+1
 lda #$00
 sta $06
P_1_65 = *+1
 lda #$00
 sta $07
P_1_66 = *+1
 lda #$00
 sta $1B
P_1_67 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_68 = *+1
 lda #$00
 sta $1B
P_1_69 = *+1
 lda #$00
 sta $1C
P_1_70 = *+1
 lda #$00
 sta $1B
P_1_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_72 = *+1
 lda #$00
 sta $09
P_1_73 = *+1
 lda #$00
 sta $06
P_1_74 = *+1
 lda #$00
 sta $07
P_1_75 = *+1
 lda #$00
 sta $1B
P_1_76 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_77 = *+1
 lda #$00
 sta $1B
P_1_78 = *+1
 lda #$00
 sta $1C
P_1_79 = *+1
 lda #$00
 sta $1B
P_1_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_81 = *+1
 lda #$00
 sta $09
P_1_82 = *+1
 lda #$00
 sta $06
P_1_83 = *+1
 lda #$00
 sta $07
P_1_84 = *+1
 lda #$00
 sta $1B
P_1_85 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_86 = *+1
 lda #$00
 sta $1B
P_1_87 = *+1
 lda #$00
 sta $1C
P_1_88 = *+1
 lda #$00
 sta $1B
P_1_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_90 = *+1
 lda #$00
 sta $09
P_1_91 = *+1
 lda #$00
 sta $06
P_1_92 = *+1
 lda #$00
 sta $07
P_1_93 = *+1
 lda #$00
 sta $1B
P_1_94 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_95 = *+1
 lda #$00
 sta $1B
P_1_96 = *+1
 lda #$00
 sta $1C
P_1_97 = *+1
 lda #$00
 sta $1B
P_1_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_99 = *+1
 lda #$00
 sta $09
P_1_100 = *+1
 lda #$00
 sta $06
P_1_101 = *+1
 lda #$00
 sta $07
P_1_102 = *+1
 lda #$00
 sta $1B
P_1_103 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_104 = *+1
 lda #$00
 sta $1B
P_1_105 = *+1
 lda #$00
 sta $1C
P_1_106 = *+1
 lda #$00
 sta $1B
P_1_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_108 = *+1
 lda #$00
 sta $09
P_1_109 = *+1
 lda #$00
 sta $06
P_1_110 = *+1
 lda #$00
 sta $07
P_1_111 = *+1
 lda #$00
 sta $1B
P_1_112 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_113 = *+1
 lda #$00
 sta $1B
P_1_114 = *+1
 lda #$00
 sta $1C
P_1_115 = *+1
 lda #$00
 sta $1B
P_1_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_117 = *+1
 lda #$00
 sta $09
P_1_118 = *+1
 lda #$00
 sta $06
P_1_119 = *+1
 lda #$00
 sta $07
P_1_120 = *+1
 lda #$00
 sta $1B
P_1_121 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_122 = *+1
 lda #$00
 sta $1B
P_1_123 = *+1
 lda #$00
 sta $1C
P_1_124 = *+1
 lda #$00
 sta $1B
P_1_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_126 = *+1
 lda #$00
 sta $09
P_1_127 = *+1
 lda #$00
 sta $06
P_1_128 = *+1
 lda #$00
 sta $07
P_1_129 = *+1
 lda #$00
 sta $1B
P_1_130 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_131 = *+1
 lda #$00
 sta $1B
P_1_132 = *+1
 lda #$00
 sta $1C
P_1_133 = *+1
 lda #$00
 sta $1B
P_1_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_135 = *+1
 lda #$00
 sta $09
P_1_136 = *+1
 lda #$00
 sta $06
P_1_137 = *+1
 lda #$00
 sta $07
P_1_138 = *+1
 lda #$00
 sta $1B
P_1_139 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_140 = *+1
 lda #$00
 sta $1B
P_1_141 = *+1
 lda #$00
 sta $1C
P_1_142 = *+1
 lda #$00
 sta $1B
P_1_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_144 = *+1
 lda #$00
 sta $09
P_1_145 = *+1
 lda #$00
 sta $06
P_1_146 = *+1
 lda #$00
 sta $07
P_1_147 = *+1
 lda #$00
 sta $1B
P_1_148 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_149 = *+1
 lda #$00
 sta $1B
P_1_150 = *+1
 lda #$00
 sta $1C
P_1_151 = *+1
 lda #$00
 sta $1B
P_1_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_153 = *+1
 lda #$00
 sta $09
P_1_154 = *+1
 lda #$00
 sta $06
P_1_155 = *+1
 lda #$00
 sta $07
P_1_156 = *+1
 lda #$00
 sta $1B
P_1_157 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_158 = *+1
 lda #$00
 sta $1B
P_1_159 = *+1
 lda #$00
 sta $1C
P_1_160 = *+1
 lda #$00
 sta $1B
P_1_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_162 = *+1
 lda #$00
 sta $09
P_1_163 = *+1
 lda #$00
 sta $06
P_1_164 = *+1
 lda #$00
 sta $07
P_1_165 = *+1
 lda #$00
 sta $1B
P_1_166 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_167 = *+1
 lda #$00
 sta $1B
P_1_168 = *+1
 lda #$00
 sta $1C
P_1_169 = *+1
 lda #$00
 sta $1B
P_1_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_171 = *+1
 lda #$00
 sta $09
P_1_172 = *+1
 lda #$00
 sta $06
P_1_173 = *+1
 lda #$00
 sta $07
P_1_174 = *+1
 lda #$00
 sta $1B
P_1_175 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_176 = *+1
 lda #$00
 sta $1B
P_1_177 = *+1
 lda #$00
 sta $1C
P_1_178 = *+1
 lda #$00
 sta $1B
P_1_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_180 = *+1
 lda #$00
 sta $09
P_1_181 = *+1
 lda #$00
 sta $06
P_1_182 = *+1
 lda #$00
 sta $07
P_1_183 = *+1
 lda #$00
 sta $1B
P_1_184 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_185 = *+1
 lda #$00
 sta $1B
P_1_186 = *+1
 lda #$00
 sta $1C
P_1_187 = *+1
 lda #$00
 sta $1B
P_1_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_189 = *+1
 lda #$00
 sta $09
P_1_190 = *+1
 lda #$00
 sta $06
P_1_191 = *+1
 lda #$00
 sta $07
P_1_192 = *+1
 lda #$00
 sta $1B
P_1_193 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_194 = *+1
 lda #$00
 sta $1B
P_1_195 = *+1
 lda #$00
 sta $1C
P_1_196 = *+1
 lda #$00
 sta $1B
P_1_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_198 = *+1
 lda #$00
 sta $09
P_1_199 = *+1
 lda #$00
 sta $06
P_1_200 = *+1
 lda #$00
 sta $07
P_1_201 = *+1
 lda #$00
 sta $1B
P_1_202 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_203 = *+1
 lda #$00
 sta $1B
P_1_204 = *+1
 lda #$00
 sta $1C
P_1_205 = *+1
 lda #$00
 sta $1B
P_1_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_207 = *+1
 lda #$00
 sta $09
P_1_208 = *+1
 lda #$00
 sta $06
P_1_209 = *+1
 lda #$00
 sta $07
P_1_210 = *+1
 lda #$00
 sta $1B
P_1_211 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_212 = *+1
 lda #$00
 sta $1B
P_1_213 = *+1
 lda #$00
 sta $1C
P_1_214 = *+1
 lda #$00
 sta $1B
P_1_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_216 = *+1
 lda #$00
 sta $09
P_1_217 = *+1
 lda #$00
 sta $06
P_1_218 = *+1
 lda #$00
 sta $07
P_1_219 = *+1
 lda #$00
 sta $1B
P_1_220 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_221 = *+1
 lda #$00
 sta $1B
P_1_222 = *+1
 lda #$00
 sta $1C
P_1_223 = *+1
 lda #$00
 sta $1B
P_1_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_225 = *+1
 lda #$00
 sta $09
P_1_226 = *+1
 lda #$00
 sta $06
P_1_227 = *+1
 lda #$00
 sta $07
P_1_228 = *+1
 lda #$00
 sta $1B
P_1_229 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_230 = *+1
 lda #$00
 sta $1B
P_1_231 = *+1
 lda #$00
 sta $1C
P_1_232 = *+1
 lda #$00
 sta $1B
P_1_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_234 = *+1
 lda #$00
 sta $09
P_1_235 = *+1
 lda #$00
 sta $06
P_1_236 = *+1
 lda #$00
 sta $07
P_1_237 = *+1
 lda #$00
 sta $1B
P_1_238 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_239 = *+1
 lda #$00
 sta $1B
P_1_240 = *+1
 lda #$00
 sta $1C
P_1_241 = *+1
 lda #$00
 sta $1B
P_1_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_243 = *+1
 lda #$00
 sta $09
P_1_244 = *+1
 lda #$00
 sta $06
P_1_245 = *+1
 lda #$00
 sta $07
P_1_246 = *+1
 lda #$00
 sta $1B
P_1_247 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_248 = *+1
 lda #$00
 sta $1B
P_1_249 = *+1
 lda #$00
 sta $1C
P_1_250 = *+1
 lda #$00
 sta $1B
P_1_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_252 = *+1
 lda #$00
 sta $09
P_1_253 = *+1
 lda #$00
 sta $06
P_1_254 = *+1
 lda #$00
 sta $07
P_1_255 = *+1
 lda #$00
 sta $1B
P_1_256 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_257 = *+1
 lda #$00
 sta $1B
P_1_258 = *+1
 lda #$00
 sta $1C
P_1_259 = *+1
 lda #$00
 sta $1B
P_1_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_261 = *+1
 lda #$00
 sta $09
P_1_262 = *+1
 lda #$00
 sta $06
P_1_263 = *+1
 lda #$00
 sta $07
P_1_264 = *+1
 lda #$00
 sta $1B
P_1_265 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_266 = *+1
 lda #$00
 sta $1B
P_1_267 = *+1
 lda #$00
 sta $1C
P_1_268 = *+1
 lda #$00
 sta $1B
P_1_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_270 = *+1
 lda #$00
 sta $09
P_1_271 = *+1
 lda #$00
 sta $06
P_1_272 = *+1
 lda #$00
 sta $07
P_1_273 = *+1
 lda #$00
 sta $1B
P_1_274 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_275 = *+1
 lda #$00
 sta $1B
P_1_276 = *+1
 lda #$00
 sta $1C
P_1_277 = *+1
 lda #$00
 sta $1B
P_1_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_279 = *+1
 lda #$00
 sta $09
P_1_280 = *+1
 lda #$00
 sta $06
P_1_281 = *+1
 lda #$00
 sta $07
P_1_282 = *+1
 lda #$00
 sta $1B
P_1_283 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_284 = *+1
 lda #$00
 sta $1B
P_1_285 = *+1
 lda #$00
 sta $1C
P_1_286 = *+1
 lda #$00
 sta $1B
P_1_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_288 = *+1
 lda #$00
 sta $09
P_1_289 = *+1
 lda #$00
 sta $06
P_1_290 = *+1
 lda #$00
 sta $07
P_1_291 = *+1
 lda #$00
 sta $1B
P_1_292 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_293 = *+1
 lda #$00
 sta $1B
P_1_294 = *+1
 lda #$00
 sta $1C
P_1_295 = *+1
 lda #$00
 sta $1B
P_1_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_297 = *+1
 lda #$00
 sta $09
P_1_298 = *+1
 lda #$00
 sta $06
P_1_299 = *+1
 lda #$00
 sta $07
P_1_300 = *+1
 lda #$00
 sta $1B
P_1_301 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_302 = *+1
 lda #$00
 sta $1B
P_1_303 = *+1
 lda #$00
 sta $1C
P_1_304 = *+1
 lda #$00
 sta $1B
P_1_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_306 = *+1
 lda #$00
 sta $09
P_1_307 = *+1
 lda #$00
 sta $06
P_1_308 = *+1
 lda #$00
 sta $07
P_1_309 = *+1
 lda #$00
 sta $1B
P_1_310 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_311 = *+1
 lda #$00
 sta $1B
P_1_312 = *+1
 lda #$00
 sta $1C
P_1_313 = *+1
 lda #$00
 sta $1B
P_1_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_315 = *+1
 lda #$00
 sta $09
P_1_316 = *+1
 lda #$00
 sta $06
P_1_317 = *+1
 lda #$00
 sta $07
P_1_318 = *+1
 lda #$00
 sta $1B
P_1_319 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_320 = *+1
 lda #$00
 sta $1B
P_1_321 = *+1
 lda #$00
 sta $1C
P_1_322 = *+1
 lda #$00
 sta $1B
P_1_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_324 = *+1
 lda #$00
 sta $09
P_1_325 = *+1
 lda #$00
 sta $06
P_1_326 = *+1
 lda #$00
 sta $07
P_1_327 = *+1
 lda #$00
 sta $1B
P_1_328 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_329 = *+1
 lda #$00
 sta $1B
P_1_330 = *+1
 lda #$00
 sta $1C
P_1_331 = *+1
 lda #$00
 sta $1B
P_1_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_333 = *+1
 lda #$00
 sta $09
P_1_334 = *+1
 lda #$00
 sta $06
P_1_335 = *+1
 lda #$00
 sta $07
P_1_336 = *+1
 lda #$00
 sta $1B
P_1_337 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_338 = *+1
 lda #$00
 sta $1B
P_1_339 = *+1
 lda #$00
 sta $1C
P_1_340 = *+1
 lda #$00
 sta $1B
P_1_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_342 = *+1
 lda #$00
 sta $09
P_1_343 = *+1
 lda #$00
 sta $06
P_1_344 = *+1
 lda #$00
 sta $07
P_1_345 = *+1
 lda #$00
 sta $1B
P_1_346 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_347 = *+1
 lda #$00
 sta $1B
P_1_348 = *+1
 lda #$00
 sta $1C
P_1_349 = *+1
 lda #$00
 sta $1B
P_1_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_351 = *+1
 lda #$00
 sta $09
P_1_352 = *+1
 lda #$00
 sta $06
P_1_353 = *+1
 lda #$00
 sta $07
P_1_354 = *+1
 lda #$00
 sta $1B
P_1_355 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_356 = *+1
 lda #$00
 sta $1B
P_1_357 = *+1
 lda #$00
 sta $1C
P_1_358 = *+1
 lda #$00
 sta $1B
P_1_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_360 = *+1
 lda #$00
 sta $09
P_1_361 = *+1
 lda #$00
 sta $06
P_1_362 = *+1
 lda #$00
 sta $07
P_1_363 = *+1
 lda #$00
 sta $1B
P_1_364 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_365 = *+1
 lda #$00
 sta $1B
P_1_366 = *+1
 lda #$00
 sta $1C
P_1_367 = *+1
 lda #$00
 sta $1B
P_1_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_369 = *+1
 lda #$00
 sta $09
P_1_370 = *+1
 lda #$00
 sta $06
P_1_371 = *+1
 lda #$00
 sta $07
P_1_372 = *+1
 lda #$00
 sta $1B
P_1_373 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_374 = *+1
 lda #$00
 sta $1B
P_1_375 = *+1
 lda #$00
 sta $1C
P_1_376 = *+1
 lda #$00
 sta $1B
P_1_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_378 = *+1
 lda #$00
 sta $09
P_1_379 = *+1
 lda #$00
 sta $06
P_1_380 = *+1
 lda #$00
 sta $07
P_1_381 = *+1
 lda #$00
 sta $1B
P_1_382 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_383 = *+1
 lda #$00
 sta $1B
P_1_384 = *+1
 lda #$00
 sta $1C
P_1_385 = *+1
 lda #$00
 sta $1B
P_1_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_387 = *+1
 lda #$00
 sta $09
P_1_388 = *+1
 lda #$00
 sta $06
P_1_389 = *+1
 lda #$00
 sta $07
P_1_390 = *+1
 lda #$00
 sta $1B
P_1_391 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_392 = *+1
 lda #$00
 sta $1B
P_1_393 = *+1
 lda #$00
 sta $1C
P_1_394 = *+1
 lda #$00
 sta $1B
P_1_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_396 = *+1
 lda #$00
 sta $09
P_1_397 = *+1
 lda #$00
 sta $06
P_1_398 = *+1
 lda #$00
 sta $07
P_1_399 = *+1
 lda #$00
 sta $1B
P_1_400 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_401 = *+1
 lda #$00
 sta $1B
P_1_402 = *+1
 lda #$00
 sta $1C
P_1_403 = *+1
 lda #$00
 sta $1B
P_1_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_405 = *+1
 lda #$00
 sta $09
P_1_406 = *+1
 lda #$00
 sta $06
P_1_407 = *+1
 lda #$00
 sta $07
P_1_408 = *+1
 lda #$00
 sta $1B
P_1_409 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_410 = *+1
 lda #$00
 sta $1B
P_1_411 = *+1
 lda #$00
 sta $1C
P_1_412 = *+1
 lda #$00
 sta $1B
P_1_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_414 = *+1
 lda #$00
 sta $09
P_1_415 = *+1
 lda #$00
 sta $06
P_1_416 = *+1
 lda #$00
 sta $07
P_1_417 = *+1
 lda #$00
 sta $1B
P_1_418 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_419 = *+1
 lda #$00
 sta $1B
P_1_420 = *+1
 lda #$00
 sta $1C
P_1_421 = *+1
 lda #$00
 sta $1B
P_1_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_423 = *+1
 lda #$00
 sta $09
P_1_424 = *+1
 lda #$00
 sta $06
P_1_425 = *+1
 lda #$00
 sta $07
P_1_426 = *+1
 lda #$00
 sta $1B
P_1_427 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_428 = *+1
 lda #$00
 sta $1B
P_1_429 = *+1
 lda #$00
 sta $1C
P_1_430 = *+1
 lda #$00
 sta $1B
P_1_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_432 = *+1
 lda #$00
 sta $09
P_1_433 = *+1
 lda #$00
 sta $06
P_1_434 = *+1
 lda #$00
 sta $07
P_1_435 = *+1
 lda #$00
 sta $1B
P_1_436 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_437 = *+1
 lda #$00
 sta $1B
P_1_438 = *+1
 lda #$00
 sta $1C
P_1_439 = *+1
 lda #$00
 sta $1B
P_1_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_441 = *+1
 lda #$00
 sta $09
P_1_442 = *+1
 lda #$00
 sta $06
P_1_443 = *+1
 lda #$00
 sta $07
P_1_444 = *+1
 lda #$00
 sta $1B
P_1_445 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_446 = *+1
 lda #$00
 sta $1B
P_1_447 = *+1
 lda #$00
 sta $1C
P_1_448 = *+1
 lda #$00
 sta $1B
P_1_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_450 = *+1
 lda #$00
 sta $09
P_1_451 = *+1
 lda #$00
 sta $06
P_1_452 = *+1
 lda #$00
 sta $07
P_1_453 = *+1
 lda #$00
 sta $1B
P_1_454 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_455 = *+1
 lda #$00
 sta $1B
P_1_456 = *+1
 lda #$00
 sta $1C
P_1_457 = *+1
 lda #$00
 sta $1B
P_1_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_459 = *+1
 lda #$00
 sta $09
P_1_460 = *+1
 lda #$00
 sta $06
P_1_461 = *+1
 lda #$00
 sta $07
P_1_462 = *+1
 lda #$00
 sta $1B
P_1_463 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_464 = *+1
 lda #$00
 sta $1B
P_1_465 = *+1
 lda #$00
 sta $1C
P_1_466 = *+1
 lda #$00
 sta $1B
P_1_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_468 = *+1
 lda #$00
 sta $09
P_1_469 = *+1
 lda #$00
 sta $06
P_1_470 = *+1
 lda #$00
 sta $07
P_1_471 = *+1
 lda #$00
 sta $1B
P_1_472 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_473 = *+1
 lda #$00
 sta $1B
P_1_474 = *+1
 lda #$00
 sta $1C
P_1_475 = *+1
 lda #$00
 sta $1B
P_1_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_477 = *+1
 lda #$00
 sta $09
P_1_478 = *+1
 lda #$00
 sta $06
P_1_479 = *+1
 lda #$00
 sta $07
P_1_480 = *+1
 lda #$00
 sta $1B
P_1_481 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_482 = *+1
 lda #$00
 sta $1B
P_1_483 = *+1
 lda #$00
 sta $1C
P_1_484 = *+1
 lda #$00
 sta $1B
P_1_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_486 = *+1
 lda #$00
 sta $09
P_1_487 = *+1
 lda #$00
 sta $06
P_1_488 = *+1
 lda #$00
 sta $07
P_1_489 = *+1
 lda #$00
 sta $1B
P_1_490 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_491 = *+1
 lda #$00
 sta $1B
P_1_492 = *+1
 lda #$00
 sta $1C
P_1_493 = *+1
 lda #$00
 sta $1B
P_1_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_495 = *+1
 lda #$00
 sta $09
P_1_496 = *+1
 lda #$00
 sta $06
P_1_497 = *+1
 lda #$00
 sta $07
P_1_498 = *+1
 lda #$00
 sta $1B
P_1_499 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_500 = *+1
 lda #$00
 sta $1B
P_1_501 = *+1
 lda #$00
 sta $1C
P_1_502 = *+1
 lda #$00
 sta $1B
P_1_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_504 = *+1
 lda #$00
 sta $09
P_1_505 = *+1
 lda #$00
 sta $06
P_1_506 = *+1
 lda #$00
 sta $07
P_1_507 = *+1
 lda #$00
 sta $1B
P_1_508 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_509 = *+1
 lda #$00
 sta $1B
P_1_510 = *+1
 lda #$00
 sta $1C
P_1_511 = *+1
 lda #$00
 sta $1B
P_1_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_513 = *+1
 lda #$00
 sta $09
P_1_514 = *+1
 lda #$00
 sta $06
P_1_515 = *+1
 lda #$00
 sta $07
P_1_516 = *+1
 lda #$00
 sta $1B
P_1_517 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_518 = *+1
 lda #$00
 sta $1B
P_1_519 = *+1
 lda #$00
 sta $1C
P_1_520 = *+1
 lda #$00
 sta $1B
P_1_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_522 = *+1
 lda #$00
 sta $09
P_1_523 = *+1
 lda #$00
 sta $06
P_1_524 = *+1
 lda #$00
 sta $07
P_1_525 = *+1
 lda #$00
 sta $1B
P_1_526 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_527 = *+1
 lda #$00
 sta $1B
P_1_528 = *+1
 lda #$00
 sta $1C
P_1_529 = *+1
 lda #$00
 sta $1B
P_1_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_531 = *+1
 lda #$00
 sta $09
P_1_532 = *+1
 lda #$00
 sta $06
P_1_533 = *+1
 lda #$00
 sta $07
P_1_534 = *+1
 lda #$00
 sta $1B
P_1_535 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_536 = *+1
 lda #$00
 sta $1B
P_1_537 = *+1
 lda #$00
 sta $1C
P_1_538 = *+1
 lda #$00
 sta $1B
P_1_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_540 = *+1
 lda #$00
 sta $09
P_1_541 = *+1
 lda #$00
 sta $06
P_1_542 = *+1
 lda #$00
 sta $07
P_1_543 = *+1
 lda #$00
 sta $1B
P_1_544 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_545 = *+1
 lda #$00
 sta $1B
P_1_546 = *+1
 lda #$00
 sta $1C
P_1_547 = *+1
 lda #$00
 sta $1B
P_1_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_549 = *+1
 lda #$00
 sta $09
P_1_550 = *+1
 lda #$00
 sta $06
P_1_551 = *+1
 lda #$00
 sta $07
P_1_552 = *+1
 lda #$00
 sta $1B
P_1_553 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_554 = *+1
 lda #$00
 sta $1B
P_1_555 = *+1
 lda #$00
 sta $1C
P_1_556 = *+1
 lda #$00
 sta $1B
P_1_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_558 = *+1
 lda #$00
 sta $09
P_1_559 = *+1
 lda #$00
 sta $06
P_1_560 = *+1
 lda #$00
 sta $07
P_1_561 = *+1
 lda #$00
 sta $1B
P_1_562 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_563 = *+1
 lda #$00
 sta $1B
P_1_564 = *+1
 lda #$00
 sta $1C
P_1_565 = *+1
 lda #$00
 sta $1B
P_1_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_1_567 = *+1
 lda #$00
 sta $09
P_1_568 = *+1
 lda #$00
 sta $06
P_1_569 = *+1
 lda #$00
 sta $07
P_1_570 = *+1
 lda #$00
 sta $1B
P_1_571 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_1_572 = *+1
 lda #$00
 sta $1B
P_1_573 = *+1
 lda #$00
 sta $1C
P_1_574 = *+1
 lda #$00
 sta $1B
P_1_575 = *+1
 lda #$00
 sta $1C
 jmp $FF06
 ORG $1F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $1FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $2000
 RORG $F000
 sta $02
P_2_0 = *+1
 lda #$00
 sta $09
P_2_1 = *+1
 lda #$00
 sta $06
P_2_2 = *+1
 lda #$00
 sta $07
P_2_3 = *+1
 lda #$00
 sta $1B
P_2_4 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_5 = *+1
 lda #$00
 sta $1B
P_2_6 = *+1
 lda #$00
 sta $1C
P_2_7 = *+1
 lda #$00
 sta $1B
P_2_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_9 = *+1
 lda #$00
 sta $09
P_2_10 = *+1
 lda #$00
 sta $06
P_2_11 = *+1
 lda #$00
 sta $07
P_2_12 = *+1
 lda #$00
 sta $1B
P_2_13 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_14 = *+1
 lda #$00
 sta $1B
P_2_15 = *+1
 lda #$00
 sta $1C
P_2_16 = *+1
 lda #$00
 sta $1B
P_2_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_18 = *+1
 lda #$00
 sta $09
P_2_19 = *+1
 lda #$00
 sta $06
P_2_20 = *+1
 lda #$00
 sta $07
P_2_21 = *+1
 lda #$00
 sta $1B
P_2_22 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_23 = *+1
 lda #$00
 sta $1B
P_2_24 = *+1
 lda #$00
 sta $1C
P_2_25 = *+1
 lda #$00
 sta $1B
P_2_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_27 = *+1
 lda #$00
 sta $09
P_2_28 = *+1
 lda #$00
 sta $06
P_2_29 = *+1
 lda #$00
 sta $07
P_2_30 = *+1
 lda #$00
 sta $1B
P_2_31 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_32 = *+1
 lda #$00
 sta $1B
P_2_33 = *+1
 lda #$00
 sta $1C
P_2_34 = *+1
 lda #$00
 sta $1B
P_2_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_36 = *+1
 lda #$00
 sta $09
P_2_37 = *+1
 lda #$00
 sta $06
P_2_38 = *+1
 lda #$00
 sta $07
P_2_39 = *+1
 lda #$00
 sta $1B
P_2_40 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_41 = *+1
 lda #$00
 sta $1B
P_2_42 = *+1
 lda #$00
 sta $1C
P_2_43 = *+1
 lda #$00
 sta $1B
P_2_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_45 = *+1
 lda #$00
 sta $09
P_2_46 = *+1
 lda #$00
 sta $06
P_2_47 = *+1
 lda #$00
 sta $07
P_2_48 = *+1
 lda #$00
 sta $1B
P_2_49 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_50 = *+1
 lda #$00
 sta $1B
P_2_51 = *+1
 lda #$00
 sta $1C
P_2_52 = *+1
 lda #$00
 sta $1B
P_2_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_54 = *+1
 lda #$00
 sta $09
P_2_55 = *+1
 lda #$00
 sta $06
P_2_56 = *+1
 lda #$00
 sta $07
P_2_57 = *+1
 lda #$00
 sta $1B
P_2_58 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_59 = *+1
 lda #$00
 sta $1B
P_2_60 = *+1
 lda #$00
 sta $1C
P_2_61 = *+1
 lda #$00
 sta $1B
P_2_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_63 = *+1
 lda #$00
 sta $09
P_2_64 = *+1
 lda #$00
 sta $06
P_2_65 = *+1
 lda #$00
 sta $07
P_2_66 = *+1
 lda #$00
 sta $1B
P_2_67 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_68 = *+1
 lda #$00
 sta $1B
P_2_69 = *+1
 lda #$00
 sta $1C
P_2_70 = *+1
 lda #$00
 sta $1B
P_2_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_72 = *+1
 lda #$00
 sta $09
P_2_73 = *+1
 lda #$00
 sta $06
P_2_74 = *+1
 lda #$00
 sta $07
P_2_75 = *+1
 lda #$00
 sta $1B
P_2_76 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_77 = *+1
 lda #$00
 sta $1B
P_2_78 = *+1
 lda #$00
 sta $1C
P_2_79 = *+1
 lda #$00
 sta $1B
P_2_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_81 = *+1
 lda #$00
 sta $09
P_2_82 = *+1
 lda #$00
 sta $06
P_2_83 = *+1
 lda #$00
 sta $07
P_2_84 = *+1
 lda #$00
 sta $1B
P_2_85 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_86 = *+1
 lda #$00
 sta $1B
P_2_87 = *+1
 lda #$00
 sta $1C
P_2_88 = *+1
 lda #$00
 sta $1B
P_2_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_90 = *+1
 lda #$00
 sta $09
P_2_91 = *+1
 lda #$00
 sta $06
P_2_92 = *+1
 lda #$00
 sta $07
P_2_93 = *+1
 lda #$00
 sta $1B
P_2_94 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_95 = *+1
 lda #$00
 sta $1B
P_2_96 = *+1
 lda #$00
 sta $1C
P_2_97 = *+1
 lda #$00
 sta $1B
P_2_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_99 = *+1
 lda #$00
 sta $09
P_2_100 = *+1
 lda #$00
 sta $06
P_2_101 = *+1
 lda #$00
 sta $07
P_2_102 = *+1
 lda #$00
 sta $1B
P_2_103 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_104 = *+1
 lda #$00
 sta $1B
P_2_105 = *+1
 lda #$00
 sta $1C
P_2_106 = *+1
 lda #$00
 sta $1B
P_2_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_108 = *+1
 lda #$00
 sta $09
P_2_109 = *+1
 lda #$00
 sta $06
P_2_110 = *+1
 lda #$00
 sta $07
P_2_111 = *+1
 lda #$00
 sta $1B
P_2_112 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_113 = *+1
 lda #$00
 sta $1B
P_2_114 = *+1
 lda #$00
 sta $1C
P_2_115 = *+1
 lda #$00
 sta $1B
P_2_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_117 = *+1
 lda #$00
 sta $09
P_2_118 = *+1
 lda #$00
 sta $06
P_2_119 = *+1
 lda #$00
 sta $07
P_2_120 = *+1
 lda #$00
 sta $1B
P_2_121 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_122 = *+1
 lda #$00
 sta $1B
P_2_123 = *+1
 lda #$00
 sta $1C
P_2_124 = *+1
 lda #$00
 sta $1B
P_2_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_126 = *+1
 lda #$00
 sta $09
P_2_127 = *+1
 lda #$00
 sta $06
P_2_128 = *+1
 lda #$00
 sta $07
P_2_129 = *+1
 lda #$00
 sta $1B
P_2_130 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_131 = *+1
 lda #$00
 sta $1B
P_2_132 = *+1
 lda #$00
 sta $1C
P_2_133 = *+1
 lda #$00
 sta $1B
P_2_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_135 = *+1
 lda #$00
 sta $09
P_2_136 = *+1
 lda #$00
 sta $06
P_2_137 = *+1
 lda #$00
 sta $07
P_2_138 = *+1
 lda #$00
 sta $1B
P_2_139 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_140 = *+1
 lda #$00
 sta $1B
P_2_141 = *+1
 lda #$00
 sta $1C
P_2_142 = *+1
 lda #$00
 sta $1B
P_2_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_144 = *+1
 lda #$00
 sta $09
P_2_145 = *+1
 lda #$00
 sta $06
P_2_146 = *+1
 lda #$00
 sta $07
P_2_147 = *+1
 lda #$00
 sta $1B
P_2_148 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_149 = *+1
 lda #$00
 sta $1B
P_2_150 = *+1
 lda #$00
 sta $1C
P_2_151 = *+1
 lda #$00
 sta $1B
P_2_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_153 = *+1
 lda #$00
 sta $09
P_2_154 = *+1
 lda #$00
 sta $06
P_2_155 = *+1
 lda #$00
 sta $07
P_2_156 = *+1
 lda #$00
 sta $1B
P_2_157 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_158 = *+1
 lda #$00
 sta $1B
P_2_159 = *+1
 lda #$00
 sta $1C
P_2_160 = *+1
 lda #$00
 sta $1B
P_2_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_162 = *+1
 lda #$00
 sta $09
P_2_163 = *+1
 lda #$00
 sta $06
P_2_164 = *+1
 lda #$00
 sta $07
P_2_165 = *+1
 lda #$00
 sta $1B
P_2_166 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_167 = *+1
 lda #$00
 sta $1B
P_2_168 = *+1
 lda #$00
 sta $1C
P_2_169 = *+1
 lda #$00
 sta $1B
P_2_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_171 = *+1
 lda #$00
 sta $09
P_2_172 = *+1
 lda #$00
 sta $06
P_2_173 = *+1
 lda #$00
 sta $07
P_2_174 = *+1
 lda #$00
 sta $1B
P_2_175 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_176 = *+1
 lda #$00
 sta $1B
P_2_177 = *+1
 lda #$00
 sta $1C
P_2_178 = *+1
 lda #$00
 sta $1B
P_2_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_180 = *+1
 lda #$00
 sta $09
P_2_181 = *+1
 lda #$00
 sta $06
P_2_182 = *+1
 lda #$00
 sta $07
P_2_183 = *+1
 lda #$00
 sta $1B
P_2_184 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_185 = *+1
 lda #$00
 sta $1B
P_2_186 = *+1
 lda #$00
 sta $1C
P_2_187 = *+1
 lda #$00
 sta $1B
P_2_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_189 = *+1
 lda #$00
 sta $09
P_2_190 = *+1
 lda #$00
 sta $06
P_2_191 = *+1
 lda #$00
 sta $07
P_2_192 = *+1
 lda #$00
 sta $1B
P_2_193 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_194 = *+1
 lda #$00
 sta $1B
P_2_195 = *+1
 lda #$00
 sta $1C
P_2_196 = *+1
 lda #$00
 sta $1B
P_2_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_198 = *+1
 lda #$00
 sta $09
P_2_199 = *+1
 lda #$00
 sta $06
P_2_200 = *+1
 lda #$00
 sta $07
P_2_201 = *+1
 lda #$00
 sta $1B
P_2_202 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_203 = *+1
 lda #$00
 sta $1B
P_2_204 = *+1
 lda #$00
 sta $1C
P_2_205 = *+1
 lda #$00
 sta $1B
P_2_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_207 = *+1
 lda #$00
 sta $09
P_2_208 = *+1
 lda #$00
 sta $06
P_2_209 = *+1
 lda #$00
 sta $07
P_2_210 = *+1
 lda #$00
 sta $1B
P_2_211 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_212 = *+1
 lda #$00
 sta $1B
P_2_213 = *+1
 lda #$00
 sta $1C
P_2_214 = *+1
 lda #$00
 sta $1B
P_2_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_216 = *+1
 lda #$00
 sta $09
P_2_217 = *+1
 lda #$00
 sta $06
P_2_218 = *+1
 lda #$00
 sta $07
P_2_219 = *+1
 lda #$00
 sta $1B
P_2_220 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_221 = *+1
 lda #$00
 sta $1B
P_2_222 = *+1
 lda #$00
 sta $1C
P_2_223 = *+1
 lda #$00
 sta $1B
P_2_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_225 = *+1
 lda #$00
 sta $09
P_2_226 = *+1
 lda #$00
 sta $06
P_2_227 = *+1
 lda #$00
 sta $07
P_2_228 = *+1
 lda #$00
 sta $1B
P_2_229 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_230 = *+1
 lda #$00
 sta $1B
P_2_231 = *+1
 lda #$00
 sta $1C
P_2_232 = *+1
 lda #$00
 sta $1B
P_2_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_234 = *+1
 lda #$00
 sta $09
P_2_235 = *+1
 lda #$00
 sta $06
P_2_236 = *+1
 lda #$00
 sta $07
P_2_237 = *+1
 lda #$00
 sta $1B
P_2_238 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_239 = *+1
 lda #$00
 sta $1B
P_2_240 = *+1
 lda #$00
 sta $1C
P_2_241 = *+1
 lda #$00
 sta $1B
P_2_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_243 = *+1
 lda #$00
 sta $09
P_2_244 = *+1
 lda #$00
 sta $06
P_2_245 = *+1
 lda #$00
 sta $07
P_2_246 = *+1
 lda #$00
 sta $1B
P_2_247 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_248 = *+1
 lda #$00
 sta $1B
P_2_249 = *+1
 lda #$00
 sta $1C
P_2_250 = *+1
 lda #$00
 sta $1B
P_2_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_252 = *+1
 lda #$00
 sta $09
P_2_253 = *+1
 lda #$00
 sta $06
P_2_254 = *+1
 lda #$00
 sta $07
P_2_255 = *+1
 lda #$00
 sta $1B
P_2_256 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_257 = *+1
 lda #$00
 sta $1B
P_2_258 = *+1
 lda #$00
 sta $1C
P_2_259 = *+1
 lda #$00
 sta $1B
P_2_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_261 = *+1
 lda #$00
 sta $09
P_2_262 = *+1
 lda #$00
 sta $06
P_2_263 = *+1
 lda #$00
 sta $07
P_2_264 = *+1
 lda #$00
 sta $1B
P_2_265 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_266 = *+1
 lda #$00
 sta $1B
P_2_267 = *+1
 lda #$00
 sta $1C
P_2_268 = *+1
 lda #$00
 sta $1B
P_2_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_270 = *+1
 lda #$00
 sta $09
P_2_271 = *+1
 lda #$00
 sta $06
P_2_272 = *+1
 lda #$00
 sta $07
P_2_273 = *+1
 lda #$00
 sta $1B
P_2_274 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_275 = *+1
 lda #$00
 sta $1B
P_2_276 = *+1
 lda #$00
 sta $1C
P_2_277 = *+1
 lda #$00
 sta $1B
P_2_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_279 = *+1
 lda #$00
 sta $09
P_2_280 = *+1
 lda #$00
 sta $06
P_2_281 = *+1
 lda #$00
 sta $07
P_2_282 = *+1
 lda #$00
 sta $1B
P_2_283 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_284 = *+1
 lda #$00
 sta $1B
P_2_285 = *+1
 lda #$00
 sta $1C
P_2_286 = *+1
 lda #$00
 sta $1B
P_2_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_288 = *+1
 lda #$00
 sta $09
P_2_289 = *+1
 lda #$00
 sta $06
P_2_290 = *+1
 lda #$00
 sta $07
P_2_291 = *+1
 lda #$00
 sta $1B
P_2_292 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_293 = *+1
 lda #$00
 sta $1B
P_2_294 = *+1
 lda #$00
 sta $1C
P_2_295 = *+1
 lda #$00
 sta $1B
P_2_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_297 = *+1
 lda #$00
 sta $09
P_2_298 = *+1
 lda #$00
 sta $06
P_2_299 = *+1
 lda #$00
 sta $07
P_2_300 = *+1
 lda #$00
 sta $1B
P_2_301 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_302 = *+1
 lda #$00
 sta $1B
P_2_303 = *+1
 lda #$00
 sta $1C
P_2_304 = *+1
 lda #$00
 sta $1B
P_2_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_306 = *+1
 lda #$00
 sta $09
P_2_307 = *+1
 lda #$00
 sta $06
P_2_308 = *+1
 lda #$00
 sta $07
P_2_309 = *+1
 lda #$00
 sta $1B
P_2_310 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_311 = *+1
 lda #$00
 sta $1B
P_2_312 = *+1
 lda #$00
 sta $1C
P_2_313 = *+1
 lda #$00
 sta $1B
P_2_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_315 = *+1
 lda #$00
 sta $09
P_2_316 = *+1
 lda #$00
 sta $06
P_2_317 = *+1
 lda #$00
 sta $07
P_2_318 = *+1
 lda #$00
 sta $1B
P_2_319 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_320 = *+1
 lda #$00
 sta $1B
P_2_321 = *+1
 lda #$00
 sta $1C
P_2_322 = *+1
 lda #$00
 sta $1B
P_2_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_324 = *+1
 lda #$00
 sta $09
P_2_325 = *+1
 lda #$00
 sta $06
P_2_326 = *+1
 lda #$00
 sta $07
P_2_327 = *+1
 lda #$00
 sta $1B
P_2_328 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_329 = *+1
 lda #$00
 sta $1B
P_2_330 = *+1
 lda #$00
 sta $1C
P_2_331 = *+1
 lda #$00
 sta $1B
P_2_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_333 = *+1
 lda #$00
 sta $09
P_2_334 = *+1
 lda #$00
 sta $06
P_2_335 = *+1
 lda #$00
 sta $07
P_2_336 = *+1
 lda #$00
 sta $1B
P_2_337 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_338 = *+1
 lda #$00
 sta $1B
P_2_339 = *+1
 lda #$00
 sta $1C
P_2_340 = *+1
 lda #$00
 sta $1B
P_2_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_342 = *+1
 lda #$00
 sta $09
P_2_343 = *+1
 lda #$00
 sta $06
P_2_344 = *+1
 lda #$00
 sta $07
P_2_345 = *+1
 lda #$00
 sta $1B
P_2_346 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_347 = *+1
 lda #$00
 sta $1B
P_2_348 = *+1
 lda #$00
 sta $1C
P_2_349 = *+1
 lda #$00
 sta $1B
P_2_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_351 = *+1
 lda #$00
 sta $09
P_2_352 = *+1
 lda #$00
 sta $06
P_2_353 = *+1
 lda #$00
 sta $07
P_2_354 = *+1
 lda #$00
 sta $1B
P_2_355 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_356 = *+1
 lda #$00
 sta $1B
P_2_357 = *+1
 lda #$00
 sta $1C
P_2_358 = *+1
 lda #$00
 sta $1B
P_2_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_360 = *+1
 lda #$00
 sta $09
P_2_361 = *+1
 lda #$00
 sta $06
P_2_362 = *+1
 lda #$00
 sta $07
P_2_363 = *+1
 lda #$00
 sta $1B
P_2_364 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_365 = *+1
 lda #$00
 sta $1B
P_2_366 = *+1
 lda #$00
 sta $1C
P_2_367 = *+1
 lda #$00
 sta $1B
P_2_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_369 = *+1
 lda #$00
 sta $09
P_2_370 = *+1
 lda #$00
 sta $06
P_2_371 = *+1
 lda #$00
 sta $07
P_2_372 = *+1
 lda #$00
 sta $1B
P_2_373 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_374 = *+1
 lda #$00
 sta $1B
P_2_375 = *+1
 lda #$00
 sta $1C
P_2_376 = *+1
 lda #$00
 sta $1B
P_2_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_378 = *+1
 lda #$00
 sta $09
P_2_379 = *+1
 lda #$00
 sta $06
P_2_380 = *+1
 lda #$00
 sta $07
P_2_381 = *+1
 lda #$00
 sta $1B
P_2_382 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_383 = *+1
 lda #$00
 sta $1B
P_2_384 = *+1
 lda #$00
 sta $1C
P_2_385 = *+1
 lda #$00
 sta $1B
P_2_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_387 = *+1
 lda #$00
 sta $09
P_2_388 = *+1
 lda #$00
 sta $06
P_2_389 = *+1
 lda #$00
 sta $07
P_2_390 = *+1
 lda #$00
 sta $1B
P_2_391 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_392 = *+1
 lda #$00
 sta $1B
P_2_393 = *+1
 lda #$00
 sta $1C
P_2_394 = *+1
 lda #$00
 sta $1B
P_2_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_396 = *+1
 lda #$00
 sta $09
P_2_397 = *+1
 lda #$00
 sta $06
P_2_398 = *+1
 lda #$00
 sta $07
P_2_399 = *+1
 lda #$00
 sta $1B
P_2_400 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_401 = *+1
 lda #$00
 sta $1B
P_2_402 = *+1
 lda #$00
 sta $1C
P_2_403 = *+1
 lda #$00
 sta $1B
P_2_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_405 = *+1
 lda #$00
 sta $09
P_2_406 = *+1
 lda #$00
 sta $06
P_2_407 = *+1
 lda #$00
 sta $07
P_2_408 = *+1
 lda #$00
 sta $1B
P_2_409 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_410 = *+1
 lda #$00
 sta $1B
P_2_411 = *+1
 lda #$00
 sta $1C
P_2_412 = *+1
 lda #$00
 sta $1B
P_2_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_414 = *+1
 lda #$00
 sta $09
P_2_415 = *+1
 lda #$00
 sta $06
P_2_416 = *+1
 lda #$00
 sta $07
P_2_417 = *+1
 lda #$00
 sta $1B
P_2_418 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_419 = *+1
 lda #$00
 sta $1B
P_2_420 = *+1
 lda #$00
 sta $1C
P_2_421 = *+1
 lda #$00
 sta $1B
P_2_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_423 = *+1
 lda #$00
 sta $09
P_2_424 = *+1
 lda #$00
 sta $06
P_2_425 = *+1
 lda #$00
 sta $07
P_2_426 = *+1
 lda #$00
 sta $1B
P_2_427 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_428 = *+1
 lda #$00
 sta $1B
P_2_429 = *+1
 lda #$00
 sta $1C
P_2_430 = *+1
 lda #$00
 sta $1B
P_2_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_432 = *+1
 lda #$00
 sta $09
P_2_433 = *+1
 lda #$00
 sta $06
P_2_434 = *+1
 lda #$00
 sta $07
P_2_435 = *+1
 lda #$00
 sta $1B
P_2_436 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_437 = *+1
 lda #$00
 sta $1B
P_2_438 = *+1
 lda #$00
 sta $1C
P_2_439 = *+1
 lda #$00
 sta $1B
P_2_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_441 = *+1
 lda #$00
 sta $09
P_2_442 = *+1
 lda #$00
 sta $06
P_2_443 = *+1
 lda #$00
 sta $07
P_2_444 = *+1
 lda #$00
 sta $1B
P_2_445 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_446 = *+1
 lda #$00
 sta $1B
P_2_447 = *+1
 lda #$00
 sta $1C
P_2_448 = *+1
 lda #$00
 sta $1B
P_2_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_450 = *+1
 lda #$00
 sta $09
P_2_451 = *+1
 lda #$00
 sta $06
P_2_452 = *+1
 lda #$00
 sta $07
P_2_453 = *+1
 lda #$00
 sta $1B
P_2_454 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_455 = *+1
 lda #$00
 sta $1B
P_2_456 = *+1
 lda #$00
 sta $1C
P_2_457 = *+1
 lda #$00
 sta $1B
P_2_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_459 = *+1
 lda #$00
 sta $09
P_2_460 = *+1
 lda #$00
 sta $06
P_2_461 = *+1
 lda #$00
 sta $07
P_2_462 = *+1
 lda #$00
 sta $1B
P_2_463 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_464 = *+1
 lda #$00
 sta $1B
P_2_465 = *+1
 lda #$00
 sta $1C
P_2_466 = *+1
 lda #$00
 sta $1B
P_2_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_468 = *+1
 lda #$00
 sta $09
P_2_469 = *+1
 lda #$00
 sta $06
P_2_470 = *+1
 lda #$00
 sta $07
P_2_471 = *+1
 lda #$00
 sta $1B
P_2_472 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_473 = *+1
 lda #$00
 sta $1B
P_2_474 = *+1
 lda #$00
 sta $1C
P_2_475 = *+1
 lda #$00
 sta $1B
P_2_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_477 = *+1
 lda #$00
 sta $09
P_2_478 = *+1
 lda #$00
 sta $06
P_2_479 = *+1
 lda #$00
 sta $07
P_2_480 = *+1
 lda #$00
 sta $1B
P_2_481 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_482 = *+1
 lda #$00
 sta $1B
P_2_483 = *+1
 lda #$00
 sta $1C
P_2_484 = *+1
 lda #$00
 sta $1B
P_2_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_486 = *+1
 lda #$00
 sta $09
P_2_487 = *+1
 lda #$00
 sta $06
P_2_488 = *+1
 lda #$00
 sta $07
P_2_489 = *+1
 lda #$00
 sta $1B
P_2_490 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_491 = *+1
 lda #$00
 sta $1B
P_2_492 = *+1
 lda #$00
 sta $1C
P_2_493 = *+1
 lda #$00
 sta $1B
P_2_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_495 = *+1
 lda #$00
 sta $09
P_2_496 = *+1
 lda #$00
 sta $06
P_2_497 = *+1
 lda #$00
 sta $07
P_2_498 = *+1
 lda #$00
 sta $1B
P_2_499 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_500 = *+1
 lda #$00
 sta $1B
P_2_501 = *+1
 lda #$00
 sta $1C
P_2_502 = *+1
 lda #$00
 sta $1B
P_2_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_504 = *+1
 lda #$00
 sta $09
P_2_505 = *+1
 lda #$00
 sta $06
P_2_506 = *+1
 lda #$00
 sta $07
P_2_507 = *+1
 lda #$00
 sta $1B
P_2_508 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_509 = *+1
 lda #$00
 sta $1B
P_2_510 = *+1
 lda #$00
 sta $1C
P_2_511 = *+1
 lda #$00
 sta $1B
P_2_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_513 = *+1
 lda #$00
 sta $09
P_2_514 = *+1
 lda #$00
 sta $06
P_2_515 = *+1
 lda #$00
 sta $07
P_2_516 = *+1
 lda #$00
 sta $1B
P_2_517 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_518 = *+1
 lda #$00
 sta $1B
P_2_519 = *+1
 lda #$00
 sta $1C
P_2_520 = *+1
 lda #$00
 sta $1B
P_2_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_522 = *+1
 lda #$00
 sta $09
P_2_523 = *+1
 lda #$00
 sta $06
P_2_524 = *+1
 lda #$00
 sta $07
P_2_525 = *+1
 lda #$00
 sta $1B
P_2_526 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_527 = *+1
 lda #$00
 sta $1B
P_2_528 = *+1
 lda #$00
 sta $1C
P_2_529 = *+1
 lda #$00
 sta $1B
P_2_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_531 = *+1
 lda #$00
 sta $09
P_2_532 = *+1
 lda #$00
 sta $06
P_2_533 = *+1
 lda #$00
 sta $07
P_2_534 = *+1
 lda #$00
 sta $1B
P_2_535 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_536 = *+1
 lda #$00
 sta $1B
P_2_537 = *+1
 lda #$00
 sta $1C
P_2_538 = *+1
 lda #$00
 sta $1B
P_2_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_540 = *+1
 lda #$00
 sta $09
P_2_541 = *+1
 lda #$00
 sta $06
P_2_542 = *+1
 lda #$00
 sta $07
P_2_543 = *+1
 lda #$00
 sta $1B
P_2_544 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_545 = *+1
 lda #$00
 sta $1B
P_2_546 = *+1
 lda #$00
 sta $1C
P_2_547 = *+1
 lda #$00
 sta $1B
P_2_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_549 = *+1
 lda #$00
 sta $09
P_2_550 = *+1
 lda #$00
 sta $06
P_2_551 = *+1
 lda #$00
 sta $07
P_2_552 = *+1
 lda #$00
 sta $1B
P_2_553 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_554 = *+1
 lda #$00
 sta $1B
P_2_555 = *+1
 lda #$00
 sta $1C
P_2_556 = *+1
 lda #$00
 sta $1B
P_2_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_558 = *+1
 lda #$00
 sta $09
P_2_559 = *+1
 lda #$00
 sta $06
P_2_560 = *+1
 lda #$00
 sta $07
P_2_561 = *+1
 lda #$00
 sta $1B
P_2_562 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_563 = *+1
 lda #$00
 sta $1B
P_2_564 = *+1
 lda #$00
 sta $1C
P_2_565 = *+1
 lda #$00
 sta $1B
P_2_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_2_567 = *+1
 lda #$00
 sta $09
P_2_568 = *+1
 lda #$00
 sta $06
P_2_569 = *+1
 lda #$00
 sta $07
P_2_570 = *+1
 lda #$00
 sta $1B
P_2_571 = *+1
 lda #$00
 sta $1C
 nop
 nop
 nop
 nop
 nop
P_2_572 = *+1
 lda #$00
 sta $1B
P_2_573 = *+1
 lda #$00
 sta $1C
P_2_574 = *+1
 lda #$00
 sta $1B
P_2_575 = *+1
 lda #$00
 sta $1C
 jmp $FF0C
 ORG $2F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $2FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $3000
 RORG $F000
 sta $02
P_3_0 = *+1
 lda #$00
 sta $09
P_3_1 = *+1
 lda #$00
 sta $06
P_3_2 = *+1
 lda #$00
 sta $07
P_3_3 = *+1
 lda #$00
 sta $1B
P_3_4 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_5 = *+1
 lda #$00
 sta $1B
P_3_6 = *+1
 lda #$00
 sta $1C
P_3_7 = *+1
 lda #$00
 sta $1B
P_3_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_9 = *+1
 lda #$00
 sta $09
P_3_10 = *+1
 lda #$00
 sta $06
P_3_11 = *+1
 lda #$00
 sta $07
P_3_12 = *+1
 lda #$00
 sta $1B
P_3_13 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_14 = *+1
 lda #$00
 sta $1B
P_3_15 = *+1
 lda #$00
 sta $1C
P_3_16 = *+1
 lda #$00
 sta $1B
P_3_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_18 = *+1
 lda #$00
 sta $09
P_3_19 = *+1
 lda #$00
 sta $06
P_3_20 = *+1
 lda #$00
 sta $07
P_3_21 = *+1
 lda #$00
 sta $1B
P_3_22 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_23 = *+1
 lda #$00
 sta $1B
P_3_24 = *+1
 lda #$00
 sta $1C
P_3_25 = *+1
 lda #$00
 sta $1B
P_3_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_27 = *+1
 lda #$00
 sta $09
P_3_28 = *+1
 lda #$00
 sta $06
P_3_29 = *+1
 lda #$00
 sta $07
P_3_30 = *+1
 lda #$00
 sta $1B
P_3_31 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_32 = *+1
 lda #$00
 sta $1B
P_3_33 = *+1
 lda #$00
 sta $1C
P_3_34 = *+1
 lda #$00
 sta $1B
P_3_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_36 = *+1
 lda #$00
 sta $09
P_3_37 = *+1
 lda #$00
 sta $06
P_3_38 = *+1
 lda #$00
 sta $07
P_3_39 = *+1
 lda #$00
 sta $1B
P_3_40 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_41 = *+1
 lda #$00
 sta $1B
P_3_42 = *+1
 lda #$00
 sta $1C
P_3_43 = *+1
 lda #$00
 sta $1B
P_3_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_45 = *+1
 lda #$00
 sta $09
P_3_46 = *+1
 lda #$00
 sta $06
P_3_47 = *+1
 lda #$00
 sta $07
P_3_48 = *+1
 lda #$00
 sta $1B
P_3_49 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_50 = *+1
 lda #$00
 sta $1B
P_3_51 = *+1
 lda #$00
 sta $1C
P_3_52 = *+1
 lda #$00
 sta $1B
P_3_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_54 = *+1
 lda #$00
 sta $09
P_3_55 = *+1
 lda #$00
 sta $06
P_3_56 = *+1
 lda #$00
 sta $07
P_3_57 = *+1
 lda #$00
 sta $1B
P_3_58 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_59 = *+1
 lda #$00
 sta $1B
P_3_60 = *+1
 lda #$00
 sta $1C
P_3_61 = *+1
 lda #$00
 sta $1B
P_3_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_63 = *+1
 lda #$00
 sta $09
P_3_64 = *+1
 lda #$00
 sta $06
P_3_65 = *+1
 lda #$00
 sta $07
P_3_66 = *+1
 lda #$00
 sta $1B
P_3_67 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_68 = *+1
 lda #$00
 sta $1B
P_3_69 = *+1
 lda #$00
 sta $1C
P_3_70 = *+1
 lda #$00
 sta $1B
P_3_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_72 = *+1
 lda #$00
 sta $09
P_3_73 = *+1
 lda #$00
 sta $06
P_3_74 = *+1
 lda #$00
 sta $07
P_3_75 = *+1
 lda #$00
 sta $1B
P_3_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_77 = *+1
 lda #$00
 sta $1B
P_3_78 = *+1
 lda #$00
 sta $1C
P_3_79 = *+1
 lda #$00
 sta $1B
P_3_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_81 = *+1
 lda #$00
 sta $09
P_3_82 = *+1
 lda #$00
 sta $06
P_3_83 = *+1
 lda #$00
 sta $07
P_3_84 = *+1
 lda #$00
 sta $1B
P_3_85 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_86 = *+1
 lda #$00
 sta $1B
P_3_87 = *+1
 lda #$00
 sta $1C
P_3_88 = *+1
 lda #$00
 sta $1B
P_3_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_90 = *+1
 lda #$00
 sta $09
P_3_91 = *+1
 lda #$00
 sta $06
P_3_92 = *+1
 lda #$00
 sta $07
P_3_93 = *+1
 lda #$00
 sta $1B
P_3_94 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_95 = *+1
 lda #$00
 sta $1B
P_3_96 = *+1
 lda #$00
 sta $1C
P_3_97 = *+1
 lda #$00
 sta $1B
P_3_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_99 = *+1
 lda #$00
 sta $09
P_3_100 = *+1
 lda #$00
 sta $06
P_3_101 = *+1
 lda #$00
 sta $07
P_3_102 = *+1
 lda #$00
 sta $1B
P_3_103 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_104 = *+1
 lda #$00
 sta $1B
P_3_105 = *+1
 lda #$00
 sta $1C
P_3_106 = *+1
 lda #$00
 sta $1B
P_3_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_108 = *+1
 lda #$00
 sta $09
P_3_109 = *+1
 lda #$00
 sta $06
P_3_110 = *+1
 lda #$00
 sta $07
P_3_111 = *+1
 lda #$00
 sta $1B
P_3_112 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_113 = *+1
 lda #$00
 sta $1B
P_3_114 = *+1
 lda #$00
 sta $1C
P_3_115 = *+1
 lda #$00
 sta $1B
P_3_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_117 = *+1
 lda #$00
 sta $09
P_3_118 = *+1
 lda #$00
 sta $06
P_3_119 = *+1
 lda #$00
 sta $07
P_3_120 = *+1
 lda #$00
 sta $1B
P_3_121 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_122 = *+1
 lda #$00
 sta $1B
P_3_123 = *+1
 lda #$00
 sta $1C
P_3_124 = *+1
 lda #$00
 sta $1B
P_3_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_126 = *+1
 lda #$00
 sta $09
P_3_127 = *+1
 lda #$00
 sta $06
P_3_128 = *+1
 lda #$00
 sta $07
P_3_129 = *+1
 lda #$00
 sta $1B
P_3_130 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_131 = *+1
 lda #$00
 sta $1B
P_3_132 = *+1
 lda #$00
 sta $1C
P_3_133 = *+1
 lda #$00
 sta $1B
P_3_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_135 = *+1
 lda #$00
 sta $09
P_3_136 = *+1
 lda #$00
 sta $06
P_3_137 = *+1
 lda #$00
 sta $07
P_3_138 = *+1
 lda #$00
 sta $1B
P_3_139 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_140 = *+1
 lda #$00
 sta $1B
P_3_141 = *+1
 lda #$00
 sta $1C
P_3_142 = *+1
 lda #$00
 sta $1B
P_3_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_144 = *+1
 lda #$00
 sta $09
P_3_145 = *+1
 lda #$00
 sta $06
P_3_146 = *+1
 lda #$00
 sta $07
P_3_147 = *+1
 lda #$00
 sta $1B
P_3_148 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_149 = *+1
 lda #$00
 sta $1B
P_3_150 = *+1
 lda #$00
 sta $1C
P_3_151 = *+1
 lda #$00
 sta $1B
P_3_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_153 = *+1
 lda #$00
 sta $09
P_3_154 = *+1
 lda #$00
 sta $06
P_3_155 = *+1
 lda #$00
 sta $07
P_3_156 = *+1
 lda #$00
 sta $1B
P_3_157 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_158 = *+1
 lda #$00
 sta $1B
P_3_159 = *+1
 lda #$00
 sta $1C
P_3_160 = *+1
 lda #$00
 sta $1B
P_3_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_162 = *+1
 lda #$00
 sta $09
P_3_163 = *+1
 lda #$00
 sta $06
P_3_164 = *+1
 lda #$00
 sta $07
P_3_165 = *+1
 lda #$00
 sta $1B
P_3_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_167 = *+1
 lda #$00
 sta $1B
P_3_168 = *+1
 lda #$00
 sta $1C
P_3_169 = *+1
 lda #$00
 sta $1B
P_3_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_171 = *+1
 lda #$00
 sta $09
P_3_172 = *+1
 lda #$00
 sta $06
P_3_173 = *+1
 lda #$00
 sta $07
P_3_174 = *+1
 lda #$00
 sta $1B
P_3_175 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_176 = *+1
 lda #$00
 sta $1B
P_3_177 = *+1
 lda #$00
 sta $1C
P_3_178 = *+1
 lda #$00
 sta $1B
P_3_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_180 = *+1
 lda #$00
 sta $09
P_3_181 = *+1
 lda #$00
 sta $06
P_3_182 = *+1
 lda #$00
 sta $07
P_3_183 = *+1
 lda #$00
 sta $1B
P_3_184 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_185 = *+1
 lda #$00
 sta $1B
P_3_186 = *+1
 lda #$00
 sta $1C
P_3_187 = *+1
 lda #$00
 sta $1B
P_3_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_189 = *+1
 lda #$00
 sta $09
P_3_190 = *+1
 lda #$00
 sta $06
P_3_191 = *+1
 lda #$00
 sta $07
P_3_192 = *+1
 lda #$00
 sta $1B
P_3_193 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_194 = *+1
 lda #$00
 sta $1B
P_3_195 = *+1
 lda #$00
 sta $1C
P_3_196 = *+1
 lda #$00
 sta $1B
P_3_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_198 = *+1
 lda #$00
 sta $09
P_3_199 = *+1
 lda #$00
 sta $06
P_3_200 = *+1
 lda #$00
 sta $07
P_3_201 = *+1
 lda #$00
 sta $1B
P_3_202 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_203 = *+1
 lda #$00
 sta $1B
P_3_204 = *+1
 lda #$00
 sta $1C
P_3_205 = *+1
 lda #$00
 sta $1B
P_3_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_207 = *+1
 lda #$00
 sta $09
P_3_208 = *+1
 lda #$00
 sta $06
P_3_209 = *+1
 lda #$00
 sta $07
P_3_210 = *+1
 lda #$00
 sta $1B
P_3_211 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_212 = *+1
 lda #$00
 sta $1B
P_3_213 = *+1
 lda #$00
 sta $1C
P_3_214 = *+1
 lda #$00
 sta $1B
P_3_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_216 = *+1
 lda #$00
 sta $09
P_3_217 = *+1
 lda #$00
 sta $06
P_3_218 = *+1
 lda #$00
 sta $07
P_3_219 = *+1
 lda #$00
 sta $1B
P_3_220 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_221 = *+1
 lda #$00
 sta $1B
P_3_222 = *+1
 lda #$00
 sta $1C
P_3_223 = *+1
 lda #$00
 sta $1B
P_3_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_225 = *+1
 lda #$00
 sta $09
P_3_226 = *+1
 lda #$00
 sta $06
P_3_227 = *+1
 lda #$00
 sta $07
P_3_228 = *+1
 lda #$00
 sta $1B
P_3_229 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_230 = *+1
 lda #$00
 sta $1B
P_3_231 = *+1
 lda #$00
 sta $1C
P_3_232 = *+1
 lda #$00
 sta $1B
P_3_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_234 = *+1
 lda #$00
 sta $09
P_3_235 = *+1
 lda #$00
 sta $06
P_3_236 = *+1
 lda #$00
 sta $07
P_3_237 = *+1
 lda #$00
 sta $1B
P_3_238 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_239 = *+1
 lda #$00
 sta $1B
P_3_240 = *+1
 lda #$00
 sta $1C
P_3_241 = *+1
 lda #$00
 sta $1B
P_3_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_243 = *+1
 lda #$00
 sta $09
P_3_244 = *+1
 lda #$00
 sta $06
P_3_245 = *+1
 lda #$00
 sta $07
P_3_246 = *+1
 lda #$00
 sta $1B
P_3_247 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_248 = *+1
 lda #$00
 sta $1B
P_3_249 = *+1
 lda #$00
 sta $1C
P_3_250 = *+1
 lda #$00
 sta $1B
P_3_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_252 = *+1
 lda #$00
 sta $09
P_3_253 = *+1
 lda #$00
 sta $06
P_3_254 = *+1
 lda #$00
 sta $07
P_3_255 = *+1
 lda #$00
 sta $1B
P_3_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_257 = *+1
 lda #$00
 sta $1B
P_3_258 = *+1
 lda #$00
 sta $1C
P_3_259 = *+1
 lda #$00
 sta $1B
P_3_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_261 = *+1
 lda #$00
 sta $09
P_3_262 = *+1
 lda #$00
 sta $06
P_3_263 = *+1
 lda #$00
 sta $07
P_3_264 = *+1
 lda #$00
 sta $1B
P_3_265 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_266 = *+1
 lda #$00
 sta $1B
P_3_267 = *+1
 lda #$00
 sta $1C
P_3_268 = *+1
 lda #$00
 sta $1B
P_3_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_270 = *+1
 lda #$00
 sta $09
P_3_271 = *+1
 lda #$00
 sta $06
P_3_272 = *+1
 lda #$00
 sta $07
P_3_273 = *+1
 lda #$00
 sta $1B
P_3_274 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_275 = *+1
 lda #$00
 sta $1B
P_3_276 = *+1
 lda #$00
 sta $1C
P_3_277 = *+1
 lda #$00
 sta $1B
P_3_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_279 = *+1
 lda #$00
 sta $09
P_3_280 = *+1
 lda #$00
 sta $06
P_3_281 = *+1
 lda #$00
 sta $07
P_3_282 = *+1
 lda #$00
 sta $1B
P_3_283 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_284 = *+1
 lda #$00
 sta $1B
P_3_285 = *+1
 lda #$00
 sta $1C
P_3_286 = *+1
 lda #$00
 sta $1B
P_3_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_288 = *+1
 lda #$00
 sta $09
P_3_289 = *+1
 lda #$00
 sta $06
P_3_290 = *+1
 lda #$00
 sta $07
P_3_291 = *+1
 lda #$00
 sta $1B
P_3_292 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_293 = *+1
 lda #$00
 sta $1B
P_3_294 = *+1
 lda #$00
 sta $1C
P_3_295 = *+1
 lda #$00
 sta $1B
P_3_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_297 = *+1
 lda #$00
 sta $09
P_3_298 = *+1
 lda #$00
 sta $06
P_3_299 = *+1
 lda #$00
 sta $07
P_3_300 = *+1
 lda #$00
 sta $1B
P_3_301 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_302 = *+1
 lda #$00
 sta $1B
P_3_303 = *+1
 lda #$00
 sta $1C
P_3_304 = *+1
 lda #$00
 sta $1B
P_3_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_306 = *+1
 lda #$00
 sta $09
P_3_307 = *+1
 lda #$00
 sta $06
P_3_308 = *+1
 lda #$00
 sta $07
P_3_309 = *+1
 lda #$00
 sta $1B
P_3_310 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_311 = *+1
 lda #$00
 sta $1B
P_3_312 = *+1
 lda #$00
 sta $1C
P_3_313 = *+1
 lda #$00
 sta $1B
P_3_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_315 = *+1
 lda #$00
 sta $09
P_3_316 = *+1
 lda #$00
 sta $06
P_3_317 = *+1
 lda #$00
 sta $07
P_3_318 = *+1
 lda #$00
 sta $1B
P_3_319 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_320 = *+1
 lda #$00
 sta $1B
P_3_321 = *+1
 lda #$00
 sta $1C
P_3_322 = *+1
 lda #$00
 sta $1B
P_3_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_324 = *+1
 lda #$00
 sta $09
P_3_325 = *+1
 lda #$00
 sta $06
P_3_326 = *+1
 lda #$00
 sta $07
P_3_327 = *+1
 lda #$00
 sta $1B
P_3_328 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_329 = *+1
 lda #$00
 sta $1B
P_3_330 = *+1
 lda #$00
 sta $1C
P_3_331 = *+1
 lda #$00
 sta $1B
P_3_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_333 = *+1
 lda #$00
 sta $09
P_3_334 = *+1
 lda #$00
 sta $06
P_3_335 = *+1
 lda #$00
 sta $07
P_3_336 = *+1
 lda #$00
 sta $1B
P_3_337 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_338 = *+1
 lda #$00
 sta $1B
P_3_339 = *+1
 lda #$00
 sta $1C
P_3_340 = *+1
 lda #$00
 sta $1B
P_3_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_342 = *+1
 lda #$00
 sta $09
P_3_343 = *+1
 lda #$00
 sta $06
P_3_344 = *+1
 lda #$00
 sta $07
P_3_345 = *+1
 lda #$00
 sta $1B
P_3_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_347 = *+1
 lda #$00
 sta $1B
P_3_348 = *+1
 lda #$00
 sta $1C
P_3_349 = *+1
 lda #$00
 sta $1B
P_3_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_351 = *+1
 lda #$00
 sta $09
P_3_352 = *+1
 lda #$00
 sta $06
P_3_353 = *+1
 lda #$00
 sta $07
P_3_354 = *+1
 lda #$00
 sta $1B
P_3_355 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_356 = *+1
 lda #$00
 sta $1B
P_3_357 = *+1
 lda #$00
 sta $1C
P_3_358 = *+1
 lda #$00
 sta $1B
P_3_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_360 = *+1
 lda #$00
 sta $09
P_3_361 = *+1
 lda #$00
 sta $06
P_3_362 = *+1
 lda #$00
 sta $07
P_3_363 = *+1
 lda #$00
 sta $1B
P_3_364 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_365 = *+1
 lda #$00
 sta $1B
P_3_366 = *+1
 lda #$00
 sta $1C
P_3_367 = *+1
 lda #$00
 sta $1B
P_3_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_369 = *+1
 lda #$00
 sta $09
P_3_370 = *+1
 lda #$00
 sta $06
P_3_371 = *+1
 lda #$00
 sta $07
P_3_372 = *+1
 lda #$00
 sta $1B
P_3_373 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_374 = *+1
 lda #$00
 sta $1B
P_3_375 = *+1
 lda #$00
 sta $1C
P_3_376 = *+1
 lda #$00
 sta $1B
P_3_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_378 = *+1
 lda #$00
 sta $09
P_3_379 = *+1
 lda #$00
 sta $06
P_3_380 = *+1
 lda #$00
 sta $07
P_3_381 = *+1
 lda #$00
 sta $1B
P_3_382 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_383 = *+1
 lda #$00
 sta $1B
P_3_384 = *+1
 lda #$00
 sta $1C
P_3_385 = *+1
 lda #$00
 sta $1B
P_3_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_387 = *+1
 lda #$00
 sta $09
P_3_388 = *+1
 lda #$00
 sta $06
P_3_389 = *+1
 lda #$00
 sta $07
P_3_390 = *+1
 lda #$00
 sta $1B
P_3_391 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_392 = *+1
 lda #$00
 sta $1B
P_3_393 = *+1
 lda #$00
 sta $1C
P_3_394 = *+1
 lda #$00
 sta $1B
P_3_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_396 = *+1
 lda #$00
 sta $09
P_3_397 = *+1
 lda #$00
 sta $06
P_3_398 = *+1
 lda #$00
 sta $07
P_3_399 = *+1
 lda #$00
 sta $1B
P_3_400 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_401 = *+1
 lda #$00
 sta $1B
P_3_402 = *+1
 lda #$00
 sta $1C
P_3_403 = *+1
 lda #$00
 sta $1B
P_3_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_405 = *+1
 lda #$00
 sta $09
P_3_406 = *+1
 lda #$00
 sta $06
P_3_407 = *+1
 lda #$00
 sta $07
P_3_408 = *+1
 lda #$00
 sta $1B
P_3_409 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_410 = *+1
 lda #$00
 sta $1B
P_3_411 = *+1
 lda #$00
 sta $1C
P_3_412 = *+1
 lda #$00
 sta $1B
P_3_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_414 = *+1
 lda #$00
 sta $09
P_3_415 = *+1
 lda #$00
 sta $06
P_3_416 = *+1
 lda #$00
 sta $07
P_3_417 = *+1
 lda #$00
 sta $1B
P_3_418 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_419 = *+1
 lda #$00
 sta $1B
P_3_420 = *+1
 lda #$00
 sta $1C
P_3_421 = *+1
 lda #$00
 sta $1B
P_3_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_423 = *+1
 lda #$00
 sta $09
P_3_424 = *+1
 lda #$00
 sta $06
P_3_425 = *+1
 lda #$00
 sta $07
P_3_426 = *+1
 lda #$00
 sta $1B
P_3_427 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_428 = *+1
 lda #$00
 sta $1B
P_3_429 = *+1
 lda #$00
 sta $1C
P_3_430 = *+1
 lda #$00
 sta $1B
P_3_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_432 = *+1
 lda #$00
 sta $09
P_3_433 = *+1
 lda #$00
 sta $06
P_3_434 = *+1
 lda #$00
 sta $07
P_3_435 = *+1
 lda #$00
 sta $1B
P_3_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_437 = *+1
 lda #$00
 sta $1B
P_3_438 = *+1
 lda #$00
 sta $1C
P_3_439 = *+1
 lda #$00
 sta $1B
P_3_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_441 = *+1
 lda #$00
 sta $09
P_3_442 = *+1
 lda #$00
 sta $06
P_3_443 = *+1
 lda #$00
 sta $07
P_3_444 = *+1
 lda #$00
 sta $1B
P_3_445 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_446 = *+1
 lda #$00
 sta $1B
P_3_447 = *+1
 lda #$00
 sta $1C
P_3_448 = *+1
 lda #$00
 sta $1B
P_3_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_450 = *+1
 lda #$00
 sta $09
P_3_451 = *+1
 lda #$00
 sta $06
P_3_452 = *+1
 lda #$00
 sta $07
P_3_453 = *+1
 lda #$00
 sta $1B
P_3_454 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_455 = *+1
 lda #$00
 sta $1B
P_3_456 = *+1
 lda #$00
 sta $1C
P_3_457 = *+1
 lda #$00
 sta $1B
P_3_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_459 = *+1
 lda #$00
 sta $09
P_3_460 = *+1
 lda #$00
 sta $06
P_3_461 = *+1
 lda #$00
 sta $07
P_3_462 = *+1
 lda #$00
 sta $1B
P_3_463 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_464 = *+1
 lda #$00
 sta $1B
P_3_465 = *+1
 lda #$00
 sta $1C
P_3_466 = *+1
 lda #$00
 sta $1B
P_3_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_468 = *+1
 lda #$00
 sta $09
P_3_469 = *+1
 lda #$00
 sta $06
P_3_470 = *+1
 lda #$00
 sta $07
P_3_471 = *+1
 lda #$00
 sta $1B
P_3_472 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_473 = *+1
 lda #$00
 sta $1B
P_3_474 = *+1
 lda #$00
 sta $1C
P_3_475 = *+1
 lda #$00
 sta $1B
P_3_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_477 = *+1
 lda #$00
 sta $09
P_3_478 = *+1
 lda #$00
 sta $06
P_3_479 = *+1
 lda #$00
 sta $07
P_3_480 = *+1
 lda #$00
 sta $1B
P_3_481 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_482 = *+1
 lda #$00
 sta $1B
P_3_483 = *+1
 lda #$00
 sta $1C
P_3_484 = *+1
 lda #$00
 sta $1B
P_3_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_486 = *+1
 lda #$00
 sta $09
P_3_487 = *+1
 lda #$00
 sta $06
P_3_488 = *+1
 lda #$00
 sta $07
P_3_489 = *+1
 lda #$00
 sta $1B
P_3_490 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_491 = *+1
 lda #$00
 sta $1B
P_3_492 = *+1
 lda #$00
 sta $1C
P_3_493 = *+1
 lda #$00
 sta $1B
P_3_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_495 = *+1
 lda #$00
 sta $09
P_3_496 = *+1
 lda #$00
 sta $06
P_3_497 = *+1
 lda #$00
 sta $07
P_3_498 = *+1
 lda #$00
 sta $1B
P_3_499 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_500 = *+1
 lda #$00
 sta $1B
P_3_501 = *+1
 lda #$00
 sta $1C
P_3_502 = *+1
 lda #$00
 sta $1B
P_3_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_504 = *+1
 lda #$00
 sta $09
P_3_505 = *+1
 lda #$00
 sta $06
P_3_506 = *+1
 lda #$00
 sta $07
P_3_507 = *+1
 lda #$00
 sta $1B
P_3_508 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_509 = *+1
 lda #$00
 sta $1B
P_3_510 = *+1
 lda #$00
 sta $1C
P_3_511 = *+1
 lda #$00
 sta $1B
P_3_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_513 = *+1
 lda #$00
 sta $09
P_3_514 = *+1
 lda #$00
 sta $06
P_3_515 = *+1
 lda #$00
 sta $07
P_3_516 = *+1
 lda #$00
 sta $1B
P_3_517 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_518 = *+1
 lda #$00
 sta $1B
P_3_519 = *+1
 lda #$00
 sta $1C
P_3_520 = *+1
 lda #$00
 sta $1B
P_3_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_522 = *+1
 lda #$00
 sta $09
P_3_523 = *+1
 lda #$00
 sta $06
P_3_524 = *+1
 lda #$00
 sta $07
P_3_525 = *+1
 lda #$00
 sta $1B
P_3_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_527 = *+1
 lda #$00
 sta $1B
P_3_528 = *+1
 lda #$00
 sta $1C
P_3_529 = *+1
 lda #$00
 sta $1B
P_3_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_531 = *+1
 lda #$00
 sta $09
P_3_532 = *+1
 lda #$00
 sta $06
P_3_533 = *+1
 lda #$00
 sta $07
P_3_534 = *+1
 lda #$00
 sta $1B
P_3_535 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_536 = *+1
 lda #$00
 sta $1B
P_3_537 = *+1
 lda #$00
 sta $1C
P_3_538 = *+1
 lda #$00
 sta $1B
P_3_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_540 = *+1
 lda #$00
 sta $09
P_3_541 = *+1
 lda #$00
 sta $06
P_3_542 = *+1
 lda #$00
 sta $07
P_3_543 = *+1
 lda #$00
 sta $1B
P_3_544 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_545 = *+1
 lda #$00
 sta $1B
P_3_546 = *+1
 lda #$00
 sta $1C
P_3_547 = *+1
 lda #$00
 sta $1B
P_3_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_549 = *+1
 lda #$00
 sta $09
P_3_550 = *+1
 lda #$00
 sta $06
P_3_551 = *+1
 lda #$00
 sta $07
P_3_552 = *+1
 lda #$00
 sta $1B
P_3_553 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_554 = *+1
 lda #$00
 sta $1B
P_3_555 = *+1
 lda #$00
 sta $1C
P_3_556 = *+1
 lda #$00
 sta $1B
P_3_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_558 = *+1
 lda #$00
 sta $09
P_3_559 = *+1
 lda #$00
 sta $06
P_3_560 = *+1
 lda #$00
 sta $07
P_3_561 = *+1
 lda #$00
 sta $1B
P_3_562 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_563 = *+1
 lda #$00
 sta $1B
P_3_564 = *+1
 lda #$00
 sta $1C
P_3_565 = *+1
 lda #$00
 sta $1B
P_3_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_3_567 = *+1
 lda #$00
 sta $09
P_3_568 = *+1
 lda #$00
 sta $06
P_3_569 = *+1
 lda #$00
 sta $07
P_3_570 = *+1
 lda #$00
 sta $1B
P_3_571 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_3_572 = *+1
 lda #$00
 sta $1B
P_3_573 = *+1
 lda #$00
 sta $1C
P_3_574 = *+1
 lda #$00
 sta $1B
P_3_575 = *+1
 lda #$00
 sta $1C
 jmp $FF12
 ORG $3F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $3FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $4000
 RORG $F000
 sta $02
P_4_0 = *+1
 lda #$00
 sta $09
P_4_1 = *+1
 lda #$00
 sta $06
P_4_2 = *+1
 lda #$00
 sta $07
P_4_3 = *+1
 lda #$00
 sta $1B
P_4_4 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_5 = *+1
 lda #$00
 sta $1B
P_4_6 = *+1
 lda #$00
 sta $1C
P_4_7 = *+1
 lda #$00
 sta $1B
P_4_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_9 = *+1
 lda #$00
 sta $09
P_4_10 = *+1
 lda #$00
 sta $06
P_4_11 = *+1
 lda #$00
 sta $07
P_4_12 = *+1
 lda #$00
 sta $1B
P_4_13 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_14 = *+1
 lda #$00
 sta $1B
P_4_15 = *+1
 lda #$00
 sta $1C
P_4_16 = *+1
 lda #$00
 sta $1B
P_4_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_18 = *+1
 lda #$00
 sta $09
P_4_19 = *+1
 lda #$00
 sta $06
P_4_20 = *+1
 lda #$00
 sta $07
P_4_21 = *+1
 lda #$00
 sta $1B
P_4_22 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_23 = *+1
 lda #$00
 sta $1B
P_4_24 = *+1
 lda #$00
 sta $1C
P_4_25 = *+1
 lda #$00
 sta $1B
P_4_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_27 = *+1
 lda #$00
 sta $09
P_4_28 = *+1
 lda #$00
 sta $06
P_4_29 = *+1
 lda #$00
 sta $07
P_4_30 = *+1
 lda #$00
 sta $1B
P_4_31 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_32 = *+1
 lda #$00
 sta $1B
P_4_33 = *+1
 lda #$00
 sta $1C
P_4_34 = *+1
 lda #$00
 sta $1B
P_4_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_36 = *+1
 lda #$00
 sta $09
P_4_37 = *+1
 lda #$00
 sta $06
P_4_38 = *+1
 lda #$00
 sta $07
P_4_39 = *+1
 lda #$00
 sta $1B
P_4_40 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_41 = *+1
 lda #$00
 sta $1B
P_4_42 = *+1
 lda #$00
 sta $1C
P_4_43 = *+1
 lda #$00
 sta $1B
P_4_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_45 = *+1
 lda #$00
 sta $09
P_4_46 = *+1
 lda #$00
 sta $06
P_4_47 = *+1
 lda #$00
 sta $07
P_4_48 = *+1
 lda #$00
 sta $1B
P_4_49 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_50 = *+1
 lda #$00
 sta $1B
P_4_51 = *+1
 lda #$00
 sta $1C
P_4_52 = *+1
 lda #$00
 sta $1B
P_4_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_54 = *+1
 lda #$00
 sta $09
P_4_55 = *+1
 lda #$00
 sta $06
P_4_56 = *+1
 lda #$00
 sta $07
P_4_57 = *+1
 lda #$00
 sta $1B
P_4_58 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_59 = *+1
 lda #$00
 sta $1B
P_4_60 = *+1
 lda #$00
 sta $1C
P_4_61 = *+1
 lda #$00
 sta $1B
P_4_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_63 = *+1
 lda #$00
 sta $09
P_4_64 = *+1
 lda #$00
 sta $06
P_4_65 = *+1
 lda #$00
 sta $07
P_4_66 = *+1
 lda #$00
 sta $1B
P_4_67 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_68 = *+1
 lda #$00
 sta $1B
P_4_69 = *+1
 lda #$00
 sta $1C
P_4_70 = *+1
 lda #$00
 sta $1B
P_4_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_72 = *+1
 lda #$00
 sta $09
P_4_73 = *+1
 lda #$00
 sta $06
P_4_74 = *+1
 lda #$00
 sta $07
P_4_75 = *+1
 lda #$00
 sta $1B
P_4_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_77 = *+1
 lda #$00
 sta $1B
P_4_78 = *+1
 lda #$00
 sta $1C
P_4_79 = *+1
 lda #$00
 sta $1B
P_4_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_81 = *+1
 lda #$00
 sta $09
P_4_82 = *+1
 lda #$00
 sta $06
P_4_83 = *+1
 lda #$00
 sta $07
P_4_84 = *+1
 lda #$00
 sta $1B
P_4_85 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_86 = *+1
 lda #$00
 sta $1B
P_4_87 = *+1
 lda #$00
 sta $1C
P_4_88 = *+1
 lda #$00
 sta $1B
P_4_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_90 = *+1
 lda #$00
 sta $09
P_4_91 = *+1
 lda #$00
 sta $06
P_4_92 = *+1
 lda #$00
 sta $07
P_4_93 = *+1
 lda #$00
 sta $1B
P_4_94 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_95 = *+1
 lda #$00
 sta $1B
P_4_96 = *+1
 lda #$00
 sta $1C
P_4_97 = *+1
 lda #$00
 sta $1B
P_4_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_99 = *+1
 lda #$00
 sta $09
P_4_100 = *+1
 lda #$00
 sta $06
P_4_101 = *+1
 lda #$00
 sta $07
P_4_102 = *+1
 lda #$00
 sta $1B
P_4_103 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_104 = *+1
 lda #$00
 sta $1B
P_4_105 = *+1
 lda #$00
 sta $1C
P_4_106 = *+1
 lda #$00
 sta $1B
P_4_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_108 = *+1
 lda #$00
 sta $09
P_4_109 = *+1
 lda #$00
 sta $06
P_4_110 = *+1
 lda #$00
 sta $07
P_4_111 = *+1
 lda #$00
 sta $1B
P_4_112 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_113 = *+1
 lda #$00
 sta $1B
P_4_114 = *+1
 lda #$00
 sta $1C
P_4_115 = *+1
 lda #$00
 sta $1B
P_4_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_117 = *+1
 lda #$00
 sta $09
P_4_118 = *+1
 lda #$00
 sta $06
P_4_119 = *+1
 lda #$00
 sta $07
P_4_120 = *+1
 lda #$00
 sta $1B
P_4_121 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_122 = *+1
 lda #$00
 sta $1B
P_4_123 = *+1
 lda #$00
 sta $1C
P_4_124 = *+1
 lda #$00
 sta $1B
P_4_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_126 = *+1
 lda #$00
 sta $09
P_4_127 = *+1
 lda #$00
 sta $06
P_4_128 = *+1
 lda #$00
 sta $07
P_4_129 = *+1
 lda #$00
 sta $1B
P_4_130 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_131 = *+1
 lda #$00
 sta $1B
P_4_132 = *+1
 lda #$00
 sta $1C
P_4_133 = *+1
 lda #$00
 sta $1B
P_4_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_135 = *+1
 lda #$00
 sta $09
P_4_136 = *+1
 lda #$00
 sta $06
P_4_137 = *+1
 lda #$00
 sta $07
P_4_138 = *+1
 lda #$00
 sta $1B
P_4_139 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_140 = *+1
 lda #$00
 sta $1B
P_4_141 = *+1
 lda #$00
 sta $1C
P_4_142 = *+1
 lda #$00
 sta $1B
P_4_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_144 = *+1
 lda #$00
 sta $09
P_4_145 = *+1
 lda #$00
 sta $06
P_4_146 = *+1
 lda #$00
 sta $07
P_4_147 = *+1
 lda #$00
 sta $1B
P_4_148 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_149 = *+1
 lda #$00
 sta $1B
P_4_150 = *+1
 lda #$00
 sta $1C
P_4_151 = *+1
 lda #$00
 sta $1B
P_4_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_153 = *+1
 lda #$00
 sta $09
P_4_154 = *+1
 lda #$00
 sta $06
P_4_155 = *+1
 lda #$00
 sta $07
P_4_156 = *+1
 lda #$00
 sta $1B
P_4_157 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_158 = *+1
 lda #$00
 sta $1B
P_4_159 = *+1
 lda #$00
 sta $1C
P_4_160 = *+1
 lda #$00
 sta $1B
P_4_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_162 = *+1
 lda #$00
 sta $09
P_4_163 = *+1
 lda #$00
 sta $06
P_4_164 = *+1
 lda #$00
 sta $07
P_4_165 = *+1
 lda #$00
 sta $1B
P_4_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_167 = *+1
 lda #$00
 sta $1B
P_4_168 = *+1
 lda #$00
 sta $1C
P_4_169 = *+1
 lda #$00
 sta $1B
P_4_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_171 = *+1
 lda #$00
 sta $09
P_4_172 = *+1
 lda #$00
 sta $06
P_4_173 = *+1
 lda #$00
 sta $07
P_4_174 = *+1
 lda #$00
 sta $1B
P_4_175 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_176 = *+1
 lda #$00
 sta $1B
P_4_177 = *+1
 lda #$00
 sta $1C
P_4_178 = *+1
 lda #$00
 sta $1B
P_4_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_180 = *+1
 lda #$00
 sta $09
P_4_181 = *+1
 lda #$00
 sta $06
P_4_182 = *+1
 lda #$00
 sta $07
P_4_183 = *+1
 lda #$00
 sta $1B
P_4_184 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_185 = *+1
 lda #$00
 sta $1B
P_4_186 = *+1
 lda #$00
 sta $1C
P_4_187 = *+1
 lda #$00
 sta $1B
P_4_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_189 = *+1
 lda #$00
 sta $09
P_4_190 = *+1
 lda #$00
 sta $06
P_4_191 = *+1
 lda #$00
 sta $07
P_4_192 = *+1
 lda #$00
 sta $1B
P_4_193 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_194 = *+1
 lda #$00
 sta $1B
P_4_195 = *+1
 lda #$00
 sta $1C
P_4_196 = *+1
 lda #$00
 sta $1B
P_4_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_198 = *+1
 lda #$00
 sta $09
P_4_199 = *+1
 lda #$00
 sta $06
P_4_200 = *+1
 lda #$00
 sta $07
P_4_201 = *+1
 lda #$00
 sta $1B
P_4_202 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_203 = *+1
 lda #$00
 sta $1B
P_4_204 = *+1
 lda #$00
 sta $1C
P_4_205 = *+1
 lda #$00
 sta $1B
P_4_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_207 = *+1
 lda #$00
 sta $09
P_4_208 = *+1
 lda #$00
 sta $06
P_4_209 = *+1
 lda #$00
 sta $07
P_4_210 = *+1
 lda #$00
 sta $1B
P_4_211 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_212 = *+1
 lda #$00
 sta $1B
P_4_213 = *+1
 lda #$00
 sta $1C
P_4_214 = *+1
 lda #$00
 sta $1B
P_4_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_216 = *+1
 lda #$00
 sta $09
P_4_217 = *+1
 lda #$00
 sta $06
P_4_218 = *+1
 lda #$00
 sta $07
P_4_219 = *+1
 lda #$00
 sta $1B
P_4_220 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_221 = *+1
 lda #$00
 sta $1B
P_4_222 = *+1
 lda #$00
 sta $1C
P_4_223 = *+1
 lda #$00
 sta $1B
P_4_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_225 = *+1
 lda #$00
 sta $09
P_4_226 = *+1
 lda #$00
 sta $06
P_4_227 = *+1
 lda #$00
 sta $07
P_4_228 = *+1
 lda #$00
 sta $1B
P_4_229 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_230 = *+1
 lda #$00
 sta $1B
P_4_231 = *+1
 lda #$00
 sta $1C
P_4_232 = *+1
 lda #$00
 sta $1B
P_4_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_234 = *+1
 lda #$00
 sta $09
P_4_235 = *+1
 lda #$00
 sta $06
P_4_236 = *+1
 lda #$00
 sta $07
P_4_237 = *+1
 lda #$00
 sta $1B
P_4_238 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_239 = *+1
 lda #$00
 sta $1B
P_4_240 = *+1
 lda #$00
 sta $1C
P_4_241 = *+1
 lda #$00
 sta $1B
P_4_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_243 = *+1
 lda #$00
 sta $09
P_4_244 = *+1
 lda #$00
 sta $06
P_4_245 = *+1
 lda #$00
 sta $07
P_4_246 = *+1
 lda #$00
 sta $1B
P_4_247 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_248 = *+1
 lda #$00
 sta $1B
P_4_249 = *+1
 lda #$00
 sta $1C
P_4_250 = *+1
 lda #$00
 sta $1B
P_4_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_252 = *+1
 lda #$00
 sta $09
P_4_253 = *+1
 lda #$00
 sta $06
P_4_254 = *+1
 lda #$00
 sta $07
P_4_255 = *+1
 lda #$00
 sta $1B
P_4_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_257 = *+1
 lda #$00
 sta $1B
P_4_258 = *+1
 lda #$00
 sta $1C
P_4_259 = *+1
 lda #$00
 sta $1B
P_4_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_261 = *+1
 lda #$00
 sta $09
P_4_262 = *+1
 lda #$00
 sta $06
P_4_263 = *+1
 lda #$00
 sta $07
P_4_264 = *+1
 lda #$00
 sta $1B
P_4_265 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_266 = *+1
 lda #$00
 sta $1B
P_4_267 = *+1
 lda #$00
 sta $1C
P_4_268 = *+1
 lda #$00
 sta $1B
P_4_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_270 = *+1
 lda #$00
 sta $09
P_4_271 = *+1
 lda #$00
 sta $06
P_4_272 = *+1
 lda #$00
 sta $07
P_4_273 = *+1
 lda #$00
 sta $1B
P_4_274 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_275 = *+1
 lda #$00
 sta $1B
P_4_276 = *+1
 lda #$00
 sta $1C
P_4_277 = *+1
 lda #$00
 sta $1B
P_4_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_279 = *+1
 lda #$00
 sta $09
P_4_280 = *+1
 lda #$00
 sta $06
P_4_281 = *+1
 lda #$00
 sta $07
P_4_282 = *+1
 lda #$00
 sta $1B
P_4_283 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_284 = *+1
 lda #$00
 sta $1B
P_4_285 = *+1
 lda #$00
 sta $1C
P_4_286 = *+1
 lda #$00
 sta $1B
P_4_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_288 = *+1
 lda #$00
 sta $09
P_4_289 = *+1
 lda #$00
 sta $06
P_4_290 = *+1
 lda #$00
 sta $07
P_4_291 = *+1
 lda #$00
 sta $1B
P_4_292 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_293 = *+1
 lda #$00
 sta $1B
P_4_294 = *+1
 lda #$00
 sta $1C
P_4_295 = *+1
 lda #$00
 sta $1B
P_4_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_297 = *+1
 lda #$00
 sta $09
P_4_298 = *+1
 lda #$00
 sta $06
P_4_299 = *+1
 lda #$00
 sta $07
P_4_300 = *+1
 lda #$00
 sta $1B
P_4_301 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_302 = *+1
 lda #$00
 sta $1B
P_4_303 = *+1
 lda #$00
 sta $1C
P_4_304 = *+1
 lda #$00
 sta $1B
P_4_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_306 = *+1
 lda #$00
 sta $09
P_4_307 = *+1
 lda #$00
 sta $06
P_4_308 = *+1
 lda #$00
 sta $07
P_4_309 = *+1
 lda #$00
 sta $1B
P_4_310 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_311 = *+1
 lda #$00
 sta $1B
P_4_312 = *+1
 lda #$00
 sta $1C
P_4_313 = *+1
 lda #$00
 sta $1B
P_4_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_315 = *+1
 lda #$00
 sta $09
P_4_316 = *+1
 lda #$00
 sta $06
P_4_317 = *+1
 lda #$00
 sta $07
P_4_318 = *+1
 lda #$00
 sta $1B
P_4_319 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_320 = *+1
 lda #$00
 sta $1B
P_4_321 = *+1
 lda #$00
 sta $1C
P_4_322 = *+1
 lda #$00
 sta $1B
P_4_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_324 = *+1
 lda #$00
 sta $09
P_4_325 = *+1
 lda #$00
 sta $06
P_4_326 = *+1
 lda #$00
 sta $07
P_4_327 = *+1
 lda #$00
 sta $1B
P_4_328 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_329 = *+1
 lda #$00
 sta $1B
P_4_330 = *+1
 lda #$00
 sta $1C
P_4_331 = *+1
 lda #$00
 sta $1B
P_4_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_333 = *+1
 lda #$00
 sta $09
P_4_334 = *+1
 lda #$00
 sta $06
P_4_335 = *+1
 lda #$00
 sta $07
P_4_336 = *+1
 lda #$00
 sta $1B
P_4_337 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_338 = *+1
 lda #$00
 sta $1B
P_4_339 = *+1
 lda #$00
 sta $1C
P_4_340 = *+1
 lda #$00
 sta $1B
P_4_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_342 = *+1
 lda #$00
 sta $09
P_4_343 = *+1
 lda #$00
 sta $06
P_4_344 = *+1
 lda #$00
 sta $07
P_4_345 = *+1
 lda #$00
 sta $1B
P_4_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_347 = *+1
 lda #$00
 sta $1B
P_4_348 = *+1
 lda #$00
 sta $1C
P_4_349 = *+1
 lda #$00
 sta $1B
P_4_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_351 = *+1
 lda #$00
 sta $09
P_4_352 = *+1
 lda #$00
 sta $06
P_4_353 = *+1
 lda #$00
 sta $07
P_4_354 = *+1
 lda #$00
 sta $1B
P_4_355 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_356 = *+1
 lda #$00
 sta $1B
P_4_357 = *+1
 lda #$00
 sta $1C
P_4_358 = *+1
 lda #$00
 sta $1B
P_4_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_360 = *+1
 lda #$00
 sta $09
P_4_361 = *+1
 lda #$00
 sta $06
P_4_362 = *+1
 lda #$00
 sta $07
P_4_363 = *+1
 lda #$00
 sta $1B
P_4_364 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_365 = *+1
 lda #$00
 sta $1B
P_4_366 = *+1
 lda #$00
 sta $1C
P_4_367 = *+1
 lda #$00
 sta $1B
P_4_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_369 = *+1
 lda #$00
 sta $09
P_4_370 = *+1
 lda #$00
 sta $06
P_4_371 = *+1
 lda #$00
 sta $07
P_4_372 = *+1
 lda #$00
 sta $1B
P_4_373 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_374 = *+1
 lda #$00
 sta $1B
P_4_375 = *+1
 lda #$00
 sta $1C
P_4_376 = *+1
 lda #$00
 sta $1B
P_4_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_378 = *+1
 lda #$00
 sta $09
P_4_379 = *+1
 lda #$00
 sta $06
P_4_380 = *+1
 lda #$00
 sta $07
P_4_381 = *+1
 lda #$00
 sta $1B
P_4_382 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_383 = *+1
 lda #$00
 sta $1B
P_4_384 = *+1
 lda #$00
 sta $1C
P_4_385 = *+1
 lda #$00
 sta $1B
P_4_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_387 = *+1
 lda #$00
 sta $09
P_4_388 = *+1
 lda #$00
 sta $06
P_4_389 = *+1
 lda #$00
 sta $07
P_4_390 = *+1
 lda #$00
 sta $1B
P_4_391 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_392 = *+1
 lda #$00
 sta $1B
P_4_393 = *+1
 lda #$00
 sta $1C
P_4_394 = *+1
 lda #$00
 sta $1B
P_4_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_396 = *+1
 lda #$00
 sta $09
P_4_397 = *+1
 lda #$00
 sta $06
P_4_398 = *+1
 lda #$00
 sta $07
P_4_399 = *+1
 lda #$00
 sta $1B
P_4_400 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_401 = *+1
 lda #$00
 sta $1B
P_4_402 = *+1
 lda #$00
 sta $1C
P_4_403 = *+1
 lda #$00
 sta $1B
P_4_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_405 = *+1
 lda #$00
 sta $09
P_4_406 = *+1
 lda #$00
 sta $06
P_4_407 = *+1
 lda #$00
 sta $07
P_4_408 = *+1
 lda #$00
 sta $1B
P_4_409 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_410 = *+1
 lda #$00
 sta $1B
P_4_411 = *+1
 lda #$00
 sta $1C
P_4_412 = *+1
 lda #$00
 sta $1B
P_4_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_414 = *+1
 lda #$00
 sta $09
P_4_415 = *+1
 lda #$00
 sta $06
P_4_416 = *+1
 lda #$00
 sta $07
P_4_417 = *+1
 lda #$00
 sta $1B
P_4_418 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_419 = *+1
 lda #$00
 sta $1B
P_4_420 = *+1
 lda #$00
 sta $1C
P_4_421 = *+1
 lda #$00
 sta $1B
P_4_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_423 = *+1
 lda #$00
 sta $09
P_4_424 = *+1
 lda #$00
 sta $06
P_4_425 = *+1
 lda #$00
 sta $07
P_4_426 = *+1
 lda #$00
 sta $1B
P_4_427 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_428 = *+1
 lda #$00
 sta $1B
P_4_429 = *+1
 lda #$00
 sta $1C
P_4_430 = *+1
 lda #$00
 sta $1B
P_4_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_432 = *+1
 lda #$00
 sta $09
P_4_433 = *+1
 lda #$00
 sta $06
P_4_434 = *+1
 lda #$00
 sta $07
P_4_435 = *+1
 lda #$00
 sta $1B
P_4_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_437 = *+1
 lda #$00
 sta $1B
P_4_438 = *+1
 lda #$00
 sta $1C
P_4_439 = *+1
 lda #$00
 sta $1B
P_4_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_441 = *+1
 lda #$00
 sta $09
P_4_442 = *+1
 lda #$00
 sta $06
P_4_443 = *+1
 lda #$00
 sta $07
P_4_444 = *+1
 lda #$00
 sta $1B
P_4_445 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_446 = *+1
 lda #$00
 sta $1B
P_4_447 = *+1
 lda #$00
 sta $1C
P_4_448 = *+1
 lda #$00
 sta $1B
P_4_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_450 = *+1
 lda #$00
 sta $09
P_4_451 = *+1
 lda #$00
 sta $06
P_4_452 = *+1
 lda #$00
 sta $07
P_4_453 = *+1
 lda #$00
 sta $1B
P_4_454 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_455 = *+1
 lda #$00
 sta $1B
P_4_456 = *+1
 lda #$00
 sta $1C
P_4_457 = *+1
 lda #$00
 sta $1B
P_4_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_459 = *+1
 lda #$00
 sta $09
P_4_460 = *+1
 lda #$00
 sta $06
P_4_461 = *+1
 lda #$00
 sta $07
P_4_462 = *+1
 lda #$00
 sta $1B
P_4_463 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_464 = *+1
 lda #$00
 sta $1B
P_4_465 = *+1
 lda #$00
 sta $1C
P_4_466 = *+1
 lda #$00
 sta $1B
P_4_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_468 = *+1
 lda #$00
 sta $09
P_4_469 = *+1
 lda #$00
 sta $06
P_4_470 = *+1
 lda #$00
 sta $07
P_4_471 = *+1
 lda #$00
 sta $1B
P_4_472 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_473 = *+1
 lda #$00
 sta $1B
P_4_474 = *+1
 lda #$00
 sta $1C
P_4_475 = *+1
 lda #$00
 sta $1B
P_4_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_477 = *+1
 lda #$00
 sta $09
P_4_478 = *+1
 lda #$00
 sta $06
P_4_479 = *+1
 lda #$00
 sta $07
P_4_480 = *+1
 lda #$00
 sta $1B
P_4_481 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_482 = *+1
 lda #$00
 sta $1B
P_4_483 = *+1
 lda #$00
 sta $1C
P_4_484 = *+1
 lda #$00
 sta $1B
P_4_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_486 = *+1
 lda #$00
 sta $09
P_4_487 = *+1
 lda #$00
 sta $06
P_4_488 = *+1
 lda #$00
 sta $07
P_4_489 = *+1
 lda #$00
 sta $1B
P_4_490 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_491 = *+1
 lda #$00
 sta $1B
P_4_492 = *+1
 lda #$00
 sta $1C
P_4_493 = *+1
 lda #$00
 sta $1B
P_4_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_495 = *+1
 lda #$00
 sta $09
P_4_496 = *+1
 lda #$00
 sta $06
P_4_497 = *+1
 lda #$00
 sta $07
P_4_498 = *+1
 lda #$00
 sta $1B
P_4_499 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_500 = *+1
 lda #$00
 sta $1B
P_4_501 = *+1
 lda #$00
 sta $1C
P_4_502 = *+1
 lda #$00
 sta $1B
P_4_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_504 = *+1
 lda #$00
 sta $09
P_4_505 = *+1
 lda #$00
 sta $06
P_4_506 = *+1
 lda #$00
 sta $07
P_4_507 = *+1
 lda #$00
 sta $1B
P_4_508 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_509 = *+1
 lda #$00
 sta $1B
P_4_510 = *+1
 lda #$00
 sta $1C
P_4_511 = *+1
 lda #$00
 sta $1B
P_4_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_513 = *+1
 lda #$00
 sta $09
P_4_514 = *+1
 lda #$00
 sta $06
P_4_515 = *+1
 lda #$00
 sta $07
P_4_516 = *+1
 lda #$00
 sta $1B
P_4_517 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_518 = *+1
 lda #$00
 sta $1B
P_4_519 = *+1
 lda #$00
 sta $1C
P_4_520 = *+1
 lda #$00
 sta $1B
P_4_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_522 = *+1
 lda #$00
 sta $09
P_4_523 = *+1
 lda #$00
 sta $06
P_4_524 = *+1
 lda #$00
 sta $07
P_4_525 = *+1
 lda #$00
 sta $1B
P_4_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_527 = *+1
 lda #$00
 sta $1B
P_4_528 = *+1
 lda #$00
 sta $1C
P_4_529 = *+1
 lda #$00
 sta $1B
P_4_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_531 = *+1
 lda #$00
 sta $09
P_4_532 = *+1
 lda #$00
 sta $06
P_4_533 = *+1
 lda #$00
 sta $07
P_4_534 = *+1
 lda #$00
 sta $1B
P_4_535 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_536 = *+1
 lda #$00
 sta $1B
P_4_537 = *+1
 lda #$00
 sta $1C
P_4_538 = *+1
 lda #$00
 sta $1B
P_4_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_540 = *+1
 lda #$00
 sta $09
P_4_541 = *+1
 lda #$00
 sta $06
P_4_542 = *+1
 lda #$00
 sta $07
P_4_543 = *+1
 lda #$00
 sta $1B
P_4_544 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_545 = *+1
 lda #$00
 sta $1B
P_4_546 = *+1
 lda #$00
 sta $1C
P_4_547 = *+1
 lda #$00
 sta $1B
P_4_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_549 = *+1
 lda #$00
 sta $09
P_4_550 = *+1
 lda #$00
 sta $06
P_4_551 = *+1
 lda #$00
 sta $07
P_4_552 = *+1
 lda #$00
 sta $1B
P_4_553 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_554 = *+1
 lda #$00
 sta $1B
P_4_555 = *+1
 lda #$00
 sta $1C
P_4_556 = *+1
 lda #$00
 sta $1B
P_4_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_558 = *+1
 lda #$00
 sta $09
P_4_559 = *+1
 lda #$00
 sta $06
P_4_560 = *+1
 lda #$00
 sta $07
P_4_561 = *+1
 lda #$00
 sta $1B
P_4_562 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_563 = *+1
 lda #$00
 sta $1B
P_4_564 = *+1
 lda #$00
 sta $1C
P_4_565 = *+1
 lda #$00
 sta $1B
P_4_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_4_567 = *+1
 lda #$00
 sta $09
P_4_568 = *+1
 lda #$00
 sta $06
P_4_569 = *+1
 lda #$00
 sta $07
P_4_570 = *+1
 lda #$00
 sta $1B
P_4_571 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_4_572 = *+1
 lda #$00
 sta $1B
P_4_573 = *+1
 lda #$00
 sta $1C
P_4_574 = *+1
 lda #$00
 sta $1B
P_4_575 = *+1
 lda #$00
 sta $1C
 jmp $FF18
 ORG $4F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $4FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $5000
 RORG $F000
 sta $02
P_5_0 = *+1
 lda #$00
 sta $09
P_5_1 = *+1
 lda #$00
 sta $06
P_5_2 = *+1
 lda #$00
 sta $07
P_5_3 = *+1
 lda #$00
 sta $1B
P_5_4 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_5 = *+1
 lda #$00
 sta $1B
P_5_6 = *+1
 lda #$00
 sta $1C
P_5_7 = *+1
 lda #$00
 sta $1B
P_5_8 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_9 = *+1
 lda #$00
 sta $09
P_5_10 = *+1
 lda #$00
 sta $06
P_5_11 = *+1
 lda #$00
 sta $07
P_5_12 = *+1
 lda #$00
 sta $1B
P_5_13 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_14 = *+1
 lda #$00
 sta $1B
P_5_15 = *+1
 lda #$00
 sta $1C
P_5_16 = *+1
 lda #$00
 sta $1B
P_5_17 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_18 = *+1
 lda #$00
 sta $09
P_5_19 = *+1
 lda #$00
 sta $06
P_5_20 = *+1
 lda #$00
 sta $07
P_5_21 = *+1
 lda #$00
 sta $1B
P_5_22 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_23 = *+1
 lda #$00
 sta $1B
P_5_24 = *+1
 lda #$00
 sta $1C
P_5_25 = *+1
 lda #$00
 sta $1B
P_5_26 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_27 = *+1
 lda #$00
 sta $09
P_5_28 = *+1
 lda #$00
 sta $06
P_5_29 = *+1
 lda #$00
 sta $07
P_5_30 = *+1
 lda #$00
 sta $1B
P_5_31 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_32 = *+1
 lda #$00
 sta $1B
P_5_33 = *+1
 lda #$00
 sta $1C
P_5_34 = *+1
 lda #$00
 sta $1B
P_5_35 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_36 = *+1
 lda #$00
 sta $09
P_5_37 = *+1
 lda #$00
 sta $06
P_5_38 = *+1
 lda #$00
 sta $07
P_5_39 = *+1
 lda #$00
 sta $1B
P_5_40 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_41 = *+1
 lda #$00
 sta $1B
P_5_42 = *+1
 lda #$00
 sta $1C
P_5_43 = *+1
 lda #$00
 sta $1B
P_5_44 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_45 = *+1
 lda #$00
 sta $09
P_5_46 = *+1
 lda #$00
 sta $06
P_5_47 = *+1
 lda #$00
 sta $07
P_5_48 = *+1
 lda #$00
 sta $1B
P_5_49 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_50 = *+1
 lda #$00
 sta $1B
P_5_51 = *+1
 lda #$00
 sta $1C
P_5_52 = *+1
 lda #$00
 sta $1B
P_5_53 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_54 = *+1
 lda #$00
 sta $09
P_5_55 = *+1
 lda #$00
 sta $06
P_5_56 = *+1
 lda #$00
 sta $07
P_5_57 = *+1
 lda #$00
 sta $1B
P_5_58 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_59 = *+1
 lda #$00
 sta $1B
P_5_60 = *+1
 lda #$00
 sta $1C
P_5_61 = *+1
 lda #$00
 sta $1B
P_5_62 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_63 = *+1
 lda #$00
 sta $09
P_5_64 = *+1
 lda #$00
 sta $06
P_5_65 = *+1
 lda #$00
 sta $07
P_5_66 = *+1
 lda #$00
 sta $1B
P_5_67 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_68 = *+1
 lda #$00
 sta $1B
P_5_69 = *+1
 lda #$00
 sta $1C
P_5_70 = *+1
 lda #$00
 sta $1B
P_5_71 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_72 = *+1
 lda #$00
 sta $09
P_5_73 = *+1
 lda #$00
 sta $06
P_5_74 = *+1
 lda #$00
 sta $07
P_5_75 = *+1
 lda #$00
 sta $1B
P_5_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_77 = *+1
 lda #$00
 sta $1B
P_5_78 = *+1
 lda #$00
 sta $1C
P_5_79 = *+1
 lda #$00
 sta $1B
P_5_80 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_81 = *+1
 lda #$00
 sta $09
P_5_82 = *+1
 lda #$00
 sta $06
P_5_83 = *+1
 lda #$00
 sta $07
P_5_84 = *+1
 lda #$00
 sta $1B
P_5_85 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_86 = *+1
 lda #$00
 sta $1B
P_5_87 = *+1
 lda #$00
 sta $1C
P_5_88 = *+1
 lda #$00
 sta $1B
P_5_89 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_90 = *+1
 lda #$00
 sta $09
P_5_91 = *+1
 lda #$00
 sta $06
P_5_92 = *+1
 lda #$00
 sta $07
P_5_93 = *+1
 lda #$00
 sta $1B
P_5_94 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_95 = *+1
 lda #$00
 sta $1B
P_5_96 = *+1
 lda #$00
 sta $1C
P_5_97 = *+1
 lda #$00
 sta $1B
P_5_98 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_99 = *+1
 lda #$00
 sta $09
P_5_100 = *+1
 lda #$00
 sta $06
P_5_101 = *+1
 lda #$00
 sta $07
P_5_102 = *+1
 lda #$00
 sta $1B
P_5_103 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_104 = *+1
 lda #$00
 sta $1B
P_5_105 = *+1
 lda #$00
 sta $1C
P_5_106 = *+1
 lda #$00
 sta $1B
P_5_107 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_108 = *+1
 lda #$00
 sta $09
P_5_109 = *+1
 lda #$00
 sta $06
P_5_110 = *+1
 lda #$00
 sta $07
P_5_111 = *+1
 lda #$00
 sta $1B
P_5_112 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_113 = *+1
 lda #$00
 sta $1B
P_5_114 = *+1
 lda #$00
 sta $1C
P_5_115 = *+1
 lda #$00
 sta $1B
P_5_116 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_117 = *+1
 lda #$00
 sta $09
P_5_118 = *+1
 lda #$00
 sta $06
P_5_119 = *+1
 lda #$00
 sta $07
P_5_120 = *+1
 lda #$00
 sta $1B
P_5_121 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_122 = *+1
 lda #$00
 sta $1B
P_5_123 = *+1
 lda #$00
 sta $1C
P_5_124 = *+1
 lda #$00
 sta $1B
P_5_125 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_126 = *+1
 lda #$00
 sta $09
P_5_127 = *+1
 lda #$00
 sta $06
P_5_128 = *+1
 lda #$00
 sta $07
P_5_129 = *+1
 lda #$00
 sta $1B
P_5_130 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_131 = *+1
 lda #$00
 sta $1B
P_5_132 = *+1
 lda #$00
 sta $1C
P_5_133 = *+1
 lda #$00
 sta $1B
P_5_134 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_135 = *+1
 lda #$00
 sta $09
P_5_136 = *+1
 lda #$00
 sta $06
P_5_137 = *+1
 lda #$00
 sta $07
P_5_138 = *+1
 lda #$00
 sta $1B
P_5_139 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_140 = *+1
 lda #$00
 sta $1B
P_5_141 = *+1
 lda #$00
 sta $1C
P_5_142 = *+1
 lda #$00
 sta $1B
P_5_143 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_144 = *+1
 lda #$00
 sta $09
P_5_145 = *+1
 lda #$00
 sta $06
P_5_146 = *+1
 lda #$00
 sta $07
P_5_147 = *+1
 lda #$00
 sta $1B
P_5_148 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_149 = *+1
 lda #$00
 sta $1B
P_5_150 = *+1
 lda #$00
 sta $1C
P_5_151 = *+1
 lda #$00
 sta $1B
P_5_152 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_153 = *+1
 lda #$00
 sta $09
P_5_154 = *+1
 lda #$00
 sta $06
P_5_155 = *+1
 lda #$00
 sta $07
P_5_156 = *+1
 lda #$00
 sta $1B
P_5_157 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_158 = *+1
 lda #$00
 sta $1B
P_5_159 = *+1
 lda #$00
 sta $1C
P_5_160 = *+1
 lda #$00
 sta $1B
P_5_161 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_162 = *+1
 lda #$00
 sta $09
P_5_163 = *+1
 lda #$00
 sta $06
P_5_164 = *+1
 lda #$00
 sta $07
P_5_165 = *+1
 lda #$00
 sta $1B
P_5_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_167 = *+1
 lda #$00
 sta $1B
P_5_168 = *+1
 lda #$00
 sta $1C
P_5_169 = *+1
 lda #$00
 sta $1B
P_5_170 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_171 = *+1
 lda #$00
 sta $09
P_5_172 = *+1
 lda #$00
 sta $06
P_5_173 = *+1
 lda #$00
 sta $07
P_5_174 = *+1
 lda #$00
 sta $1B
P_5_175 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_176 = *+1
 lda #$00
 sta $1B
P_5_177 = *+1
 lda #$00
 sta $1C
P_5_178 = *+1
 lda #$00
 sta $1B
P_5_179 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_180 = *+1
 lda #$00
 sta $09
P_5_181 = *+1
 lda #$00
 sta $06
P_5_182 = *+1
 lda #$00
 sta $07
P_5_183 = *+1
 lda #$00
 sta $1B
P_5_184 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_185 = *+1
 lda #$00
 sta $1B
P_5_186 = *+1
 lda #$00
 sta $1C
P_5_187 = *+1
 lda #$00
 sta $1B
P_5_188 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_189 = *+1
 lda #$00
 sta $09
P_5_190 = *+1
 lda #$00
 sta $06
P_5_191 = *+1
 lda #$00
 sta $07
P_5_192 = *+1
 lda #$00
 sta $1B
P_5_193 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_194 = *+1
 lda #$00
 sta $1B
P_5_195 = *+1
 lda #$00
 sta $1C
P_5_196 = *+1
 lda #$00
 sta $1B
P_5_197 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_198 = *+1
 lda #$00
 sta $09
P_5_199 = *+1
 lda #$00
 sta $06
P_5_200 = *+1
 lda #$00
 sta $07
P_5_201 = *+1
 lda #$00
 sta $1B
P_5_202 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_203 = *+1
 lda #$00
 sta $1B
P_5_204 = *+1
 lda #$00
 sta $1C
P_5_205 = *+1
 lda #$00
 sta $1B
P_5_206 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_207 = *+1
 lda #$00
 sta $09
P_5_208 = *+1
 lda #$00
 sta $06
P_5_209 = *+1
 lda #$00
 sta $07
P_5_210 = *+1
 lda #$00
 sta $1B
P_5_211 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_212 = *+1
 lda #$00
 sta $1B
P_5_213 = *+1
 lda #$00
 sta $1C
P_5_214 = *+1
 lda #$00
 sta $1B
P_5_215 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_216 = *+1
 lda #$00
 sta $09
P_5_217 = *+1
 lda #$00
 sta $06
P_5_218 = *+1
 lda #$00
 sta $07
P_5_219 = *+1
 lda #$00
 sta $1B
P_5_220 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_221 = *+1
 lda #$00
 sta $1B
P_5_222 = *+1
 lda #$00
 sta $1C
P_5_223 = *+1
 lda #$00
 sta $1B
P_5_224 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_225 = *+1
 lda #$00
 sta $09
P_5_226 = *+1
 lda #$00
 sta $06
P_5_227 = *+1
 lda #$00
 sta $07
P_5_228 = *+1
 lda #$00
 sta $1B
P_5_229 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_230 = *+1
 lda #$00
 sta $1B
P_5_231 = *+1
 lda #$00
 sta $1C
P_5_232 = *+1
 lda #$00
 sta $1B
P_5_233 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_234 = *+1
 lda #$00
 sta $09
P_5_235 = *+1
 lda #$00
 sta $06
P_5_236 = *+1
 lda #$00
 sta $07
P_5_237 = *+1
 lda #$00
 sta $1B
P_5_238 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_239 = *+1
 lda #$00
 sta $1B
P_5_240 = *+1
 lda #$00
 sta $1C
P_5_241 = *+1
 lda #$00
 sta $1B
P_5_242 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_243 = *+1
 lda #$00
 sta $09
P_5_244 = *+1
 lda #$00
 sta $06
P_5_245 = *+1
 lda #$00
 sta $07
P_5_246 = *+1
 lda #$00
 sta $1B
P_5_247 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_248 = *+1
 lda #$00
 sta $1B
P_5_249 = *+1
 lda #$00
 sta $1C
P_5_250 = *+1
 lda #$00
 sta $1B
P_5_251 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_252 = *+1
 lda #$00
 sta $09
P_5_253 = *+1
 lda #$00
 sta $06
P_5_254 = *+1
 lda #$00
 sta $07
P_5_255 = *+1
 lda #$00
 sta $1B
P_5_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_257 = *+1
 lda #$00
 sta $1B
P_5_258 = *+1
 lda #$00
 sta $1C
P_5_259 = *+1
 lda #$00
 sta $1B
P_5_260 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_261 = *+1
 lda #$00
 sta $09
P_5_262 = *+1
 lda #$00
 sta $06
P_5_263 = *+1
 lda #$00
 sta $07
P_5_264 = *+1
 lda #$00
 sta $1B
P_5_265 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_266 = *+1
 lda #$00
 sta $1B
P_5_267 = *+1
 lda #$00
 sta $1C
P_5_268 = *+1
 lda #$00
 sta $1B
P_5_269 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_270 = *+1
 lda #$00
 sta $09
P_5_271 = *+1
 lda #$00
 sta $06
P_5_272 = *+1
 lda #$00
 sta $07
P_5_273 = *+1
 lda #$00
 sta $1B
P_5_274 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_275 = *+1
 lda #$00
 sta $1B
P_5_276 = *+1
 lda #$00
 sta $1C
P_5_277 = *+1
 lda #$00
 sta $1B
P_5_278 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_279 = *+1
 lda #$00
 sta $09
P_5_280 = *+1
 lda #$00
 sta $06
P_5_281 = *+1
 lda #$00
 sta $07
P_5_282 = *+1
 lda #$00
 sta $1B
P_5_283 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_284 = *+1
 lda #$00
 sta $1B
P_5_285 = *+1
 lda #$00
 sta $1C
P_5_286 = *+1
 lda #$00
 sta $1B
P_5_287 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_288 = *+1
 lda #$00
 sta $09
P_5_289 = *+1
 lda #$00
 sta $06
P_5_290 = *+1
 lda #$00
 sta $07
P_5_291 = *+1
 lda #$00
 sta $1B
P_5_292 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_293 = *+1
 lda #$00
 sta $1B
P_5_294 = *+1
 lda #$00
 sta $1C
P_5_295 = *+1
 lda #$00
 sta $1B
P_5_296 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_297 = *+1
 lda #$00
 sta $09
P_5_298 = *+1
 lda #$00
 sta $06
P_5_299 = *+1
 lda #$00
 sta $07
P_5_300 = *+1
 lda #$00
 sta $1B
P_5_301 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_302 = *+1
 lda #$00
 sta $1B
P_5_303 = *+1
 lda #$00
 sta $1C
P_5_304 = *+1
 lda #$00
 sta $1B
P_5_305 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_306 = *+1
 lda #$00
 sta $09
P_5_307 = *+1
 lda #$00
 sta $06
P_5_308 = *+1
 lda #$00
 sta $07
P_5_309 = *+1
 lda #$00
 sta $1B
P_5_310 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_311 = *+1
 lda #$00
 sta $1B
P_5_312 = *+1
 lda #$00
 sta $1C
P_5_313 = *+1
 lda #$00
 sta $1B
P_5_314 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_315 = *+1
 lda #$00
 sta $09
P_5_316 = *+1
 lda #$00
 sta $06
P_5_317 = *+1
 lda #$00
 sta $07
P_5_318 = *+1
 lda #$00
 sta $1B
P_5_319 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_320 = *+1
 lda #$00
 sta $1B
P_5_321 = *+1
 lda #$00
 sta $1C
P_5_322 = *+1
 lda #$00
 sta $1B
P_5_323 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_324 = *+1
 lda #$00
 sta $09
P_5_325 = *+1
 lda #$00
 sta $06
P_5_326 = *+1
 lda #$00
 sta $07
P_5_327 = *+1
 lda #$00
 sta $1B
P_5_328 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_329 = *+1
 lda #$00
 sta $1B
P_5_330 = *+1
 lda #$00
 sta $1C
P_5_331 = *+1
 lda #$00
 sta $1B
P_5_332 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_333 = *+1
 lda #$00
 sta $09
P_5_334 = *+1
 lda #$00
 sta $06
P_5_335 = *+1
 lda #$00
 sta $07
P_5_336 = *+1
 lda #$00
 sta $1B
P_5_337 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_338 = *+1
 lda #$00
 sta $1B
P_5_339 = *+1
 lda #$00
 sta $1C
P_5_340 = *+1
 lda #$00
 sta $1B
P_5_341 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_342 = *+1
 lda #$00
 sta $09
P_5_343 = *+1
 lda #$00
 sta $06
P_5_344 = *+1
 lda #$00
 sta $07
P_5_345 = *+1
 lda #$00
 sta $1B
P_5_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_347 = *+1
 lda #$00
 sta $1B
P_5_348 = *+1
 lda #$00
 sta $1C
P_5_349 = *+1
 lda #$00
 sta $1B
P_5_350 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_351 = *+1
 lda #$00
 sta $09
P_5_352 = *+1
 lda #$00
 sta $06
P_5_353 = *+1
 lda #$00
 sta $07
P_5_354 = *+1
 lda #$00
 sta $1B
P_5_355 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_356 = *+1
 lda #$00
 sta $1B
P_5_357 = *+1
 lda #$00
 sta $1C
P_5_358 = *+1
 lda #$00
 sta $1B
P_5_359 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_360 = *+1
 lda #$00
 sta $09
P_5_361 = *+1
 lda #$00
 sta $06
P_5_362 = *+1
 lda #$00
 sta $07
P_5_363 = *+1
 lda #$00
 sta $1B
P_5_364 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_365 = *+1
 lda #$00
 sta $1B
P_5_366 = *+1
 lda #$00
 sta $1C
P_5_367 = *+1
 lda #$00
 sta $1B
P_5_368 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_369 = *+1
 lda #$00
 sta $09
P_5_370 = *+1
 lda #$00
 sta $06
P_5_371 = *+1
 lda #$00
 sta $07
P_5_372 = *+1
 lda #$00
 sta $1B
P_5_373 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_374 = *+1
 lda #$00
 sta $1B
P_5_375 = *+1
 lda #$00
 sta $1C
P_5_376 = *+1
 lda #$00
 sta $1B
P_5_377 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_378 = *+1
 lda #$00
 sta $09
P_5_379 = *+1
 lda #$00
 sta $06
P_5_380 = *+1
 lda #$00
 sta $07
P_5_381 = *+1
 lda #$00
 sta $1B
P_5_382 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_383 = *+1
 lda #$00
 sta $1B
P_5_384 = *+1
 lda #$00
 sta $1C
P_5_385 = *+1
 lda #$00
 sta $1B
P_5_386 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_387 = *+1
 lda #$00
 sta $09
P_5_388 = *+1
 lda #$00
 sta $06
P_5_389 = *+1
 lda #$00
 sta $07
P_5_390 = *+1
 lda #$00
 sta $1B
P_5_391 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_392 = *+1
 lda #$00
 sta $1B
P_5_393 = *+1
 lda #$00
 sta $1C
P_5_394 = *+1
 lda #$00
 sta $1B
P_5_395 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_396 = *+1
 lda #$00
 sta $09
P_5_397 = *+1
 lda #$00
 sta $06
P_5_398 = *+1
 lda #$00
 sta $07
P_5_399 = *+1
 lda #$00
 sta $1B
P_5_400 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_401 = *+1
 lda #$00
 sta $1B
P_5_402 = *+1
 lda #$00
 sta $1C
P_5_403 = *+1
 lda #$00
 sta $1B
P_5_404 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_405 = *+1
 lda #$00
 sta $09
P_5_406 = *+1
 lda #$00
 sta $06
P_5_407 = *+1
 lda #$00
 sta $07
P_5_408 = *+1
 lda #$00
 sta $1B
P_5_409 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_410 = *+1
 lda #$00
 sta $1B
P_5_411 = *+1
 lda #$00
 sta $1C
P_5_412 = *+1
 lda #$00
 sta $1B
P_5_413 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_414 = *+1
 lda #$00
 sta $09
P_5_415 = *+1
 lda #$00
 sta $06
P_5_416 = *+1
 lda #$00
 sta $07
P_5_417 = *+1
 lda #$00
 sta $1B
P_5_418 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_419 = *+1
 lda #$00
 sta $1B
P_5_420 = *+1
 lda #$00
 sta $1C
P_5_421 = *+1
 lda #$00
 sta $1B
P_5_422 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_423 = *+1
 lda #$00
 sta $09
P_5_424 = *+1
 lda #$00
 sta $06
P_5_425 = *+1
 lda #$00
 sta $07
P_5_426 = *+1
 lda #$00
 sta $1B
P_5_427 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_428 = *+1
 lda #$00
 sta $1B
P_5_429 = *+1
 lda #$00
 sta $1C
P_5_430 = *+1
 lda #$00
 sta $1B
P_5_431 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_432 = *+1
 lda #$00
 sta $09
P_5_433 = *+1
 lda #$00
 sta $06
P_5_434 = *+1
 lda #$00
 sta $07
P_5_435 = *+1
 lda #$00
 sta $1B
P_5_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_437 = *+1
 lda #$00
 sta $1B
P_5_438 = *+1
 lda #$00
 sta $1C
P_5_439 = *+1
 lda #$00
 sta $1B
P_5_440 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_441 = *+1
 lda #$00
 sta $09
P_5_442 = *+1
 lda #$00
 sta $06
P_5_443 = *+1
 lda #$00
 sta $07
P_5_444 = *+1
 lda #$00
 sta $1B
P_5_445 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_446 = *+1
 lda #$00
 sta $1B
P_5_447 = *+1
 lda #$00
 sta $1C
P_5_448 = *+1
 lda #$00
 sta $1B
P_5_449 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_450 = *+1
 lda #$00
 sta $09
P_5_451 = *+1
 lda #$00
 sta $06
P_5_452 = *+1
 lda #$00
 sta $07
P_5_453 = *+1
 lda #$00
 sta $1B
P_5_454 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_455 = *+1
 lda #$00
 sta $1B
P_5_456 = *+1
 lda #$00
 sta $1C
P_5_457 = *+1
 lda #$00
 sta $1B
P_5_458 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_459 = *+1
 lda #$00
 sta $09
P_5_460 = *+1
 lda #$00
 sta $06
P_5_461 = *+1
 lda #$00
 sta $07
P_5_462 = *+1
 lda #$00
 sta $1B
P_5_463 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_464 = *+1
 lda #$00
 sta $1B
P_5_465 = *+1
 lda #$00
 sta $1C
P_5_466 = *+1
 lda #$00
 sta $1B
P_5_467 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_468 = *+1
 lda #$00
 sta $09
P_5_469 = *+1
 lda #$00
 sta $06
P_5_470 = *+1
 lda #$00
 sta $07
P_5_471 = *+1
 lda #$00
 sta $1B
P_5_472 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_473 = *+1
 lda #$00
 sta $1B
P_5_474 = *+1
 lda #$00
 sta $1C
P_5_475 = *+1
 lda #$00
 sta $1B
P_5_476 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_477 = *+1
 lda #$00
 sta $09
P_5_478 = *+1
 lda #$00
 sta $06
P_5_479 = *+1
 lda #$00
 sta $07
P_5_480 = *+1
 lda #$00
 sta $1B
P_5_481 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_482 = *+1
 lda #$00
 sta $1B
P_5_483 = *+1
 lda #$00
 sta $1C
P_5_484 = *+1
 lda #$00
 sta $1B
P_5_485 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_486 = *+1
 lda #$00
 sta $09
P_5_487 = *+1
 lda #$00
 sta $06
P_5_488 = *+1
 lda #$00
 sta $07
P_5_489 = *+1
 lda #$00
 sta $1B
P_5_490 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_491 = *+1
 lda #$00
 sta $1B
P_5_492 = *+1
 lda #$00
 sta $1C
P_5_493 = *+1
 lda #$00
 sta $1B
P_5_494 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_495 = *+1
 lda #$00
 sta $09
P_5_496 = *+1
 lda #$00
 sta $06
P_5_497 = *+1
 lda #$00
 sta $07
P_5_498 = *+1
 lda #$00
 sta $1B
P_5_499 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_500 = *+1
 lda #$00
 sta $1B
P_5_501 = *+1
 lda #$00
 sta $1C
P_5_502 = *+1
 lda #$00
 sta $1B
P_5_503 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_504 = *+1
 lda #$00
 sta $09
P_5_505 = *+1
 lda #$00
 sta $06
P_5_506 = *+1
 lda #$00
 sta $07
P_5_507 = *+1
 lda #$00
 sta $1B
P_5_508 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_509 = *+1
 lda #$00
 sta $1B
P_5_510 = *+1
 lda #$00
 sta $1C
P_5_511 = *+1
 lda #$00
 sta $1B
P_5_512 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_513 = *+1
 lda #$00
 sta $09
P_5_514 = *+1
 lda #$00
 sta $06
P_5_515 = *+1
 lda #$00
 sta $07
P_5_516 = *+1
 lda #$00
 sta $1B
P_5_517 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_518 = *+1
 lda #$00
 sta $1B
P_5_519 = *+1
 lda #$00
 sta $1C
P_5_520 = *+1
 lda #$00
 sta $1B
P_5_521 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_522 = *+1
 lda #$00
 sta $09
P_5_523 = *+1
 lda #$00
 sta $06
P_5_524 = *+1
 lda #$00
 sta $07
P_5_525 = *+1
 lda #$00
 sta $1B
P_5_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_527 = *+1
 lda #$00
 sta $1B
P_5_528 = *+1
 lda #$00
 sta $1C
P_5_529 = *+1
 lda #$00
 sta $1B
P_5_530 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_531 = *+1
 lda #$00
 sta $09
P_5_532 = *+1
 lda #$00
 sta $06
P_5_533 = *+1
 lda #$00
 sta $07
P_5_534 = *+1
 lda #$00
 sta $1B
P_5_535 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_536 = *+1
 lda #$00
 sta $1B
P_5_537 = *+1
 lda #$00
 sta $1C
P_5_538 = *+1
 lda #$00
 sta $1B
P_5_539 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_540 = *+1
 lda #$00
 sta $09
P_5_541 = *+1
 lda #$00
 sta $06
P_5_542 = *+1
 lda #$00
 sta $07
P_5_543 = *+1
 lda #$00
 sta $1B
P_5_544 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_545 = *+1
 lda #$00
 sta $1B
P_5_546 = *+1
 lda #$00
 sta $1C
P_5_547 = *+1
 lda #$00
 sta $1B
P_5_548 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_549 = *+1
 lda #$00
 sta $09
P_5_550 = *+1
 lda #$00
 sta $06
P_5_551 = *+1
 lda #$00
 sta $07
P_5_552 = *+1
 lda #$00
 sta $1B
P_5_553 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_554 = *+1
 lda #$00
 sta $1B
P_5_555 = *+1
 lda #$00
 sta $1C
P_5_556 = *+1
 lda #$00
 sta $1B
P_5_557 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_558 = *+1
 lda #$00
 sta $09
P_5_559 = *+1
 lda #$00
 sta $06
P_5_560 = *+1
 lda #$00
 sta $07
P_5_561 = *+1
 lda #$00
 sta $1B
P_5_562 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_563 = *+1
 lda #$00
 sta $1B
P_5_564 = *+1
 lda #$00
 sta $1C
P_5_565 = *+1
 lda #$00
 sta $1B
P_5_566 = *+1
 lda #$00
 sta $1C
 sta $02
P_5_567 = *+1
 lda #$00
 sta $09
P_5_568 = *+1
 lda #$00
 sta $06
P_5_569 = *+1
 lda #$00
 sta $07
P_5_570 = *+1
 lda #$00
 sta $1B
P_5_571 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
 nop
 nop
 nop
 nop
 nop
P_5_572 = *+1
 lda #$00
 sta $1B
P_5_573 = *+1
 lda #$00
 sta $1C
P_5_574 = *+1
 lda #$00
 sta $1B
P_5_575 = *+1
 lda #$00
 sta $1C
 jmp $FF1E
 ORG $5F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $5FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $6000
 RORG $F000
 ORG $6F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $6FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 ORG $7000
 RORG $F000
Init
 sei
 cld
 ldx #$FF
 txs
 lda #0
Clear
 sta 0,x
 dex
 bne Clear
 lda #6
 sta $04
 sta $05
Frame
 lda #2
 sta $01
 sta $00
 sta $02
 sta $02
 sta $02
 lda #0
 sta $00
 lda $82
 asl
 asl
 asl
 asl
 clc
 adc #32
 ldx #0
 jsr Position
 lda $82
 asl
 asl
 asl
 asl
 clc
 adc #40
 ldx #1
 jsr Position
 sta $02
 sta $2A
 ldx #34
Blank
 sta $02
 dex
 bne Blank
 lda #0
 sta $01
 lda $82
 bne StartB
 jmp $FF24
StartB
 jmp $FF2A
 ORG $7180
 RORG $F180
Position
 sec
 sbc #3
 sta $02
 sec
Coarse
 sbc #15
 bcs Coarse
 eor #7
 asl
 asl
 asl
 asl
 sta $20,x
 sta $10,x
 rts
 ORG $7200
 RORG $F200
Overscan
 sta $02
 lda #2
 sta $01
 lda #0
 sta $0D
 sta $0E
 sta $0F
 sta $1B
 sta $1C
 sta $09
 lda $82
 eor #1
 sta $82
 ldx #29
Over
 sta $02
 dex
 bne Over
 jmp Frame
 ORG $7F00
 RORG $FF00
 lda $FFF5
 jmp $F000
 lda $FFF6
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF8
 jmp $F000
 lda $FFF9
 jmp $F000
 lda $FFFB
 jmp $F200
 lda $FFF4
 jmp $F000
 lda $FFF7
 jmp $F000
 lda $FFFB
 jmp $F000
 ORG $7FFA
 RORG $FFFA
 .word $FF30,$FF30,$FF30
 END
