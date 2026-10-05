; Atari 2600 Image Optimizer: Hybrid playfield + sprites; NTSC / 32K F4
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
 sta $08
P_0_2 = *+1
 lda #$00
 sta $0D
P_0_3 = *+1
 lda #$00
 sta $0E
P_0_4 = *+1
 lda #$00
 sta $0F
P_0_5 = *+1
 lda #$00
 sta $1B
P_0_6 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_7 = *+1
 lda #$00
 sta $0D
P_0_8 = *+1
 lda #$00
 sta $0E
P_0_9 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_10 = *+1
 lda #$00
 sta $09
P_0_11 = *+1
 lda #$00
 sta $08
P_0_12 = *+1
 lda #$00
 sta $0D
P_0_13 = *+1
 lda #$00
 sta $0E
P_0_14 = *+1
 lda #$00
 sta $0F
P_0_15 = *+1
 lda #$00
 sta $1B
P_0_16 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_17 = *+1
 lda #$00
 sta $0D
P_0_18 = *+1
 lda #$00
 sta $0E
P_0_19 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_20 = *+1
 lda #$00
 sta $09
P_0_21 = *+1
 lda #$00
 sta $08
P_0_22 = *+1
 lda #$00
 sta $0D
P_0_23 = *+1
 lda #$00
 sta $0E
P_0_24 = *+1
 lda #$00
 sta $0F
P_0_25 = *+1
 lda #$00
 sta $1B
P_0_26 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_27 = *+1
 lda #$00
 sta $0D
P_0_28 = *+1
 lda #$00
 sta $0E
P_0_29 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_30 = *+1
 lda #$00
 sta $09
P_0_31 = *+1
 lda #$00
 sta $08
P_0_32 = *+1
 lda #$00
 sta $0D
P_0_33 = *+1
 lda #$00
 sta $0E
P_0_34 = *+1
 lda #$00
 sta $0F
P_0_35 = *+1
 lda #$00
 sta $1B
P_0_36 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_37 = *+1
 lda #$00
 sta $0D
P_0_38 = *+1
 lda #$00
 sta $0E
P_0_39 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_40 = *+1
 lda #$00
 sta $09
P_0_41 = *+1
 lda #$00
 sta $08
P_0_42 = *+1
 lda #$00
 sta $0D
P_0_43 = *+1
 lda #$00
 sta $0E
P_0_44 = *+1
 lda #$00
 sta $0F
P_0_45 = *+1
 lda #$00
 sta $1B
P_0_46 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_47 = *+1
 lda #$00
 sta $0D
P_0_48 = *+1
 lda #$00
 sta $0E
P_0_49 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_50 = *+1
 lda #$00
 sta $09
P_0_51 = *+1
 lda #$00
 sta $08
P_0_52 = *+1
 lda #$00
 sta $0D
P_0_53 = *+1
 lda #$00
 sta $0E
P_0_54 = *+1
 lda #$00
 sta $0F
P_0_55 = *+1
 lda #$00
 sta $1B
P_0_56 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_57 = *+1
 lda #$00
 sta $0D
P_0_58 = *+1
 lda #$00
 sta $0E
P_0_59 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_60 = *+1
 lda #$00
 sta $09
P_0_61 = *+1
 lda #$00
 sta $08
P_0_62 = *+1
 lda #$00
 sta $0D
P_0_63 = *+1
 lda #$00
 sta $0E
P_0_64 = *+1
 lda #$00
 sta $0F
P_0_65 = *+1
 lda #$00
 sta $1B
P_0_66 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_67 = *+1
 lda #$00
 sta $0D
P_0_68 = *+1
 lda #$00
 sta $0E
P_0_69 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_70 = *+1
 lda #$00
 sta $09
P_0_71 = *+1
 lda #$00
 sta $08
P_0_72 = *+1
 lda #$00
 sta $0D
P_0_73 = *+1
 lda #$00
 sta $0E
P_0_74 = *+1
 lda #$00
 sta $0F
P_0_75 = *+1
 lda #$00
 sta $1B
P_0_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_77 = *+1
 lda #$00
 sta $0D
P_0_78 = *+1
 lda #$00
 sta $0E
P_0_79 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_80 = *+1
 lda #$00
 sta $09
P_0_81 = *+1
 lda #$00
 sta $08
P_0_82 = *+1
 lda #$00
 sta $0D
P_0_83 = *+1
 lda #$00
 sta $0E
P_0_84 = *+1
 lda #$00
 sta $0F
P_0_85 = *+1
 lda #$00
 sta $1B
P_0_86 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_87 = *+1
 lda #$00
 sta $0D
P_0_88 = *+1
 lda #$00
 sta $0E
P_0_89 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_90 = *+1
 lda #$00
 sta $09
P_0_91 = *+1
 lda #$00
 sta $08
P_0_92 = *+1
 lda #$00
 sta $0D
P_0_93 = *+1
 lda #$00
 sta $0E
P_0_94 = *+1
 lda #$00
 sta $0F
P_0_95 = *+1
 lda #$00
 sta $1B
P_0_96 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_97 = *+1
 lda #$00
 sta $0D
P_0_98 = *+1
 lda #$00
 sta $0E
P_0_99 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_100 = *+1
 lda #$00
 sta $09
P_0_101 = *+1
 lda #$00
 sta $08
P_0_102 = *+1
 lda #$00
 sta $0D
P_0_103 = *+1
 lda #$00
 sta $0E
P_0_104 = *+1
 lda #$00
 sta $0F
P_0_105 = *+1
 lda #$00
 sta $1B
P_0_106 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_107 = *+1
 lda #$00
 sta $0D
P_0_108 = *+1
 lda #$00
 sta $0E
P_0_109 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_110 = *+1
 lda #$00
 sta $09
P_0_111 = *+1
 lda #$00
 sta $08
P_0_112 = *+1
 lda #$00
 sta $0D
P_0_113 = *+1
 lda #$00
 sta $0E
P_0_114 = *+1
 lda #$00
 sta $0F
P_0_115 = *+1
 lda #$00
 sta $1B
P_0_116 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_117 = *+1
 lda #$00
 sta $0D
P_0_118 = *+1
 lda #$00
 sta $0E
P_0_119 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_120 = *+1
 lda #$00
 sta $09
P_0_121 = *+1
 lda #$00
 sta $08
P_0_122 = *+1
 lda #$00
 sta $0D
P_0_123 = *+1
 lda #$00
 sta $0E
P_0_124 = *+1
 lda #$00
 sta $0F
P_0_125 = *+1
 lda #$00
 sta $1B
P_0_126 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_127 = *+1
 lda #$00
 sta $0D
P_0_128 = *+1
 lda #$00
 sta $0E
P_0_129 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_130 = *+1
 lda #$00
 sta $09
P_0_131 = *+1
 lda #$00
 sta $08
P_0_132 = *+1
 lda #$00
 sta $0D
P_0_133 = *+1
 lda #$00
 sta $0E
P_0_134 = *+1
 lda #$00
 sta $0F
P_0_135 = *+1
 lda #$00
 sta $1B
P_0_136 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_137 = *+1
 lda #$00
 sta $0D
P_0_138 = *+1
 lda #$00
 sta $0E
P_0_139 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_140 = *+1
 lda #$00
 sta $09
P_0_141 = *+1
 lda #$00
 sta $08
P_0_142 = *+1
 lda #$00
 sta $0D
P_0_143 = *+1
 lda #$00
 sta $0E
P_0_144 = *+1
 lda #$00
 sta $0F
P_0_145 = *+1
 lda #$00
 sta $1B
P_0_146 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_147 = *+1
 lda #$00
 sta $0D
P_0_148 = *+1
 lda #$00
 sta $0E
P_0_149 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_150 = *+1
 lda #$00
 sta $09
P_0_151 = *+1
 lda #$00
 sta $08
P_0_152 = *+1
 lda #$00
 sta $0D
P_0_153 = *+1
 lda #$00
 sta $0E
P_0_154 = *+1
 lda #$00
 sta $0F
P_0_155 = *+1
 lda #$00
 sta $1B
P_0_156 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_157 = *+1
 lda #$00
 sta $0D
P_0_158 = *+1
 lda #$00
 sta $0E
P_0_159 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_160 = *+1
 lda #$00
 sta $09
P_0_161 = *+1
 lda #$00
 sta $08
P_0_162 = *+1
 lda #$00
 sta $0D
P_0_163 = *+1
 lda #$00
 sta $0E
P_0_164 = *+1
 lda #$00
 sta $0F
P_0_165 = *+1
 lda #$00
 sta $1B
P_0_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_167 = *+1
 lda #$00
 sta $0D
P_0_168 = *+1
 lda #$00
 sta $0E
P_0_169 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_170 = *+1
 lda #$00
 sta $09
P_0_171 = *+1
 lda #$00
 sta $08
P_0_172 = *+1
 lda #$00
 sta $0D
P_0_173 = *+1
 lda #$00
 sta $0E
P_0_174 = *+1
 lda #$00
 sta $0F
P_0_175 = *+1
 lda #$00
 sta $1B
P_0_176 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_177 = *+1
 lda #$00
 sta $0D
P_0_178 = *+1
 lda #$00
 sta $0E
P_0_179 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_180 = *+1
 lda #$00
 sta $09
P_0_181 = *+1
 lda #$00
 sta $08
P_0_182 = *+1
 lda #$00
 sta $0D
P_0_183 = *+1
 lda #$00
 sta $0E
P_0_184 = *+1
 lda #$00
 sta $0F
P_0_185 = *+1
 lda #$00
 sta $1B
P_0_186 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_187 = *+1
 lda #$00
 sta $0D
P_0_188 = *+1
 lda #$00
 sta $0E
P_0_189 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_190 = *+1
 lda #$00
 sta $09
P_0_191 = *+1
 lda #$00
 sta $08
P_0_192 = *+1
 lda #$00
 sta $0D
P_0_193 = *+1
 lda #$00
 sta $0E
P_0_194 = *+1
 lda #$00
 sta $0F
P_0_195 = *+1
 lda #$00
 sta $1B
P_0_196 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_197 = *+1
 lda #$00
 sta $0D
P_0_198 = *+1
 lda #$00
 sta $0E
P_0_199 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_200 = *+1
 lda #$00
 sta $09
P_0_201 = *+1
 lda #$00
 sta $08
P_0_202 = *+1
 lda #$00
 sta $0D
P_0_203 = *+1
 lda #$00
 sta $0E
P_0_204 = *+1
 lda #$00
 sta $0F
P_0_205 = *+1
 lda #$00
 sta $1B
P_0_206 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_207 = *+1
 lda #$00
 sta $0D
P_0_208 = *+1
 lda #$00
 sta $0E
P_0_209 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_210 = *+1
 lda #$00
 sta $09
P_0_211 = *+1
 lda #$00
 sta $08
P_0_212 = *+1
 lda #$00
 sta $0D
P_0_213 = *+1
 lda #$00
 sta $0E
P_0_214 = *+1
 lda #$00
 sta $0F
P_0_215 = *+1
 lda #$00
 sta $1B
P_0_216 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_217 = *+1
 lda #$00
 sta $0D
P_0_218 = *+1
 lda #$00
 sta $0E
P_0_219 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_220 = *+1
 lda #$00
 sta $09
P_0_221 = *+1
 lda #$00
 sta $08
P_0_222 = *+1
 lda #$00
 sta $0D
P_0_223 = *+1
 lda #$00
 sta $0E
P_0_224 = *+1
 lda #$00
 sta $0F
P_0_225 = *+1
 lda #$00
 sta $1B
P_0_226 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_227 = *+1
 lda #$00
 sta $0D
P_0_228 = *+1
 lda #$00
 sta $0E
P_0_229 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_230 = *+1
 lda #$00
 sta $09
P_0_231 = *+1
 lda #$00
 sta $08
P_0_232 = *+1
 lda #$00
 sta $0D
P_0_233 = *+1
 lda #$00
 sta $0E
P_0_234 = *+1
 lda #$00
 sta $0F
P_0_235 = *+1
 lda #$00
 sta $1B
P_0_236 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_237 = *+1
 lda #$00
 sta $0D
P_0_238 = *+1
 lda #$00
 sta $0E
P_0_239 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_240 = *+1
 lda #$00
 sta $09
P_0_241 = *+1
 lda #$00
 sta $08
P_0_242 = *+1
 lda #$00
 sta $0D
P_0_243 = *+1
 lda #$00
 sta $0E
P_0_244 = *+1
 lda #$00
 sta $0F
P_0_245 = *+1
 lda #$00
 sta $1B
P_0_246 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_247 = *+1
 lda #$00
 sta $0D
P_0_248 = *+1
 lda #$00
 sta $0E
P_0_249 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_250 = *+1
 lda #$00
 sta $09
P_0_251 = *+1
 lda #$00
 sta $08
P_0_252 = *+1
 lda #$00
 sta $0D
P_0_253 = *+1
 lda #$00
 sta $0E
P_0_254 = *+1
 lda #$00
 sta $0F
P_0_255 = *+1
 lda #$00
 sta $1B
P_0_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_257 = *+1
 lda #$00
 sta $0D
P_0_258 = *+1
 lda #$00
 sta $0E
P_0_259 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_260 = *+1
 lda #$00
 sta $09
P_0_261 = *+1
 lda #$00
 sta $08
P_0_262 = *+1
 lda #$00
 sta $0D
P_0_263 = *+1
 lda #$00
 sta $0E
P_0_264 = *+1
 lda #$00
 sta $0F
P_0_265 = *+1
 lda #$00
 sta $1B
P_0_266 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_267 = *+1
 lda #$00
 sta $0D
P_0_268 = *+1
 lda #$00
 sta $0E
P_0_269 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_270 = *+1
 lda #$00
 sta $09
P_0_271 = *+1
 lda #$00
 sta $08
P_0_272 = *+1
 lda #$00
 sta $0D
P_0_273 = *+1
 lda #$00
 sta $0E
P_0_274 = *+1
 lda #$00
 sta $0F
P_0_275 = *+1
 lda #$00
 sta $1B
P_0_276 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_277 = *+1
 lda #$00
 sta $0D
P_0_278 = *+1
 lda #$00
 sta $0E
P_0_279 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_280 = *+1
 lda #$00
 sta $09
P_0_281 = *+1
 lda #$00
 sta $08
P_0_282 = *+1
 lda #$00
 sta $0D
P_0_283 = *+1
 lda #$00
 sta $0E
P_0_284 = *+1
 lda #$00
 sta $0F
P_0_285 = *+1
 lda #$00
 sta $1B
P_0_286 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_287 = *+1
 lda #$00
 sta $0D
P_0_288 = *+1
 lda #$00
 sta $0E
P_0_289 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_290 = *+1
 lda #$00
 sta $09
P_0_291 = *+1
 lda #$00
 sta $08
P_0_292 = *+1
 lda #$00
 sta $0D
P_0_293 = *+1
 lda #$00
 sta $0E
P_0_294 = *+1
 lda #$00
 sta $0F
P_0_295 = *+1
 lda #$00
 sta $1B
P_0_296 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_297 = *+1
 lda #$00
 sta $0D
P_0_298 = *+1
 lda #$00
 sta $0E
P_0_299 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_300 = *+1
 lda #$00
 sta $09
P_0_301 = *+1
 lda #$00
 sta $08
P_0_302 = *+1
 lda #$00
 sta $0D
P_0_303 = *+1
 lda #$00
 sta $0E
P_0_304 = *+1
 lda #$00
 sta $0F
P_0_305 = *+1
 lda #$00
 sta $1B
P_0_306 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_307 = *+1
 lda #$00
 sta $0D
P_0_308 = *+1
 lda #$00
 sta $0E
P_0_309 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_310 = *+1
 lda #$00
 sta $09
P_0_311 = *+1
 lda #$00
 sta $08
P_0_312 = *+1
 lda #$00
 sta $0D
P_0_313 = *+1
 lda #$00
 sta $0E
P_0_314 = *+1
 lda #$00
 sta $0F
P_0_315 = *+1
 lda #$00
 sta $1B
P_0_316 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_317 = *+1
 lda #$00
 sta $0D
P_0_318 = *+1
 lda #$00
 sta $0E
P_0_319 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_320 = *+1
 lda #$00
 sta $09
P_0_321 = *+1
 lda #$00
 sta $08
P_0_322 = *+1
 lda #$00
 sta $0D
P_0_323 = *+1
 lda #$00
 sta $0E
P_0_324 = *+1
 lda #$00
 sta $0F
P_0_325 = *+1
 lda #$00
 sta $1B
P_0_326 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_327 = *+1
 lda #$00
 sta $0D
P_0_328 = *+1
 lda #$00
 sta $0E
P_0_329 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_330 = *+1
 lda #$00
 sta $09
P_0_331 = *+1
 lda #$00
 sta $08
P_0_332 = *+1
 lda #$00
 sta $0D
P_0_333 = *+1
 lda #$00
 sta $0E
P_0_334 = *+1
 lda #$00
 sta $0F
P_0_335 = *+1
 lda #$00
 sta $1B
P_0_336 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_337 = *+1
 lda #$00
 sta $0D
P_0_338 = *+1
 lda #$00
 sta $0E
P_0_339 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_340 = *+1
 lda #$00
 sta $09
P_0_341 = *+1
 lda #$00
 sta $08
P_0_342 = *+1
 lda #$00
 sta $0D
P_0_343 = *+1
 lda #$00
 sta $0E
P_0_344 = *+1
 lda #$00
 sta $0F
P_0_345 = *+1
 lda #$00
 sta $1B
P_0_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_347 = *+1
 lda #$00
 sta $0D
P_0_348 = *+1
 lda #$00
 sta $0E
P_0_349 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_350 = *+1
 lda #$00
 sta $09
P_0_351 = *+1
 lda #$00
 sta $08
P_0_352 = *+1
 lda #$00
 sta $0D
P_0_353 = *+1
 lda #$00
 sta $0E
P_0_354 = *+1
 lda #$00
 sta $0F
P_0_355 = *+1
 lda #$00
 sta $1B
P_0_356 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_357 = *+1
 lda #$00
 sta $0D
P_0_358 = *+1
 lda #$00
 sta $0E
P_0_359 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_360 = *+1
 lda #$00
 sta $09
P_0_361 = *+1
 lda #$00
 sta $08
P_0_362 = *+1
 lda #$00
 sta $0D
P_0_363 = *+1
 lda #$00
 sta $0E
P_0_364 = *+1
 lda #$00
 sta $0F
P_0_365 = *+1
 lda #$00
 sta $1B
P_0_366 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_367 = *+1
 lda #$00
 sta $0D
P_0_368 = *+1
 lda #$00
 sta $0E
P_0_369 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_370 = *+1
 lda #$00
 sta $09
P_0_371 = *+1
 lda #$00
 sta $08
P_0_372 = *+1
 lda #$00
 sta $0D
P_0_373 = *+1
 lda #$00
 sta $0E
P_0_374 = *+1
 lda #$00
 sta $0F
P_0_375 = *+1
 lda #$00
 sta $1B
P_0_376 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_377 = *+1
 lda #$00
 sta $0D
P_0_378 = *+1
 lda #$00
 sta $0E
P_0_379 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_380 = *+1
 lda #$00
 sta $09
P_0_381 = *+1
 lda #$00
 sta $08
P_0_382 = *+1
 lda #$00
 sta $0D
P_0_383 = *+1
 lda #$00
 sta $0E
P_0_384 = *+1
 lda #$00
 sta $0F
P_0_385 = *+1
 lda #$00
 sta $1B
P_0_386 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_387 = *+1
 lda #$00
 sta $0D
P_0_388 = *+1
 lda #$00
 sta $0E
P_0_389 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_390 = *+1
 lda #$00
 sta $09
P_0_391 = *+1
 lda #$00
 sta $08
P_0_392 = *+1
 lda #$00
 sta $0D
P_0_393 = *+1
 lda #$00
 sta $0E
P_0_394 = *+1
 lda #$00
 sta $0F
P_0_395 = *+1
 lda #$00
 sta $1B
P_0_396 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_397 = *+1
 lda #$00
 sta $0D
P_0_398 = *+1
 lda #$00
 sta $0E
P_0_399 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_400 = *+1
 lda #$00
 sta $09
P_0_401 = *+1
 lda #$00
 sta $08
P_0_402 = *+1
 lda #$00
 sta $0D
P_0_403 = *+1
 lda #$00
 sta $0E
P_0_404 = *+1
 lda #$00
 sta $0F
P_0_405 = *+1
 lda #$00
 sta $1B
P_0_406 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_407 = *+1
 lda #$00
 sta $0D
P_0_408 = *+1
 lda #$00
 sta $0E
P_0_409 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_410 = *+1
 lda #$00
 sta $09
P_0_411 = *+1
 lda #$00
 sta $08
P_0_412 = *+1
 lda #$00
 sta $0D
P_0_413 = *+1
 lda #$00
 sta $0E
P_0_414 = *+1
 lda #$00
 sta $0F
P_0_415 = *+1
 lda #$00
 sta $1B
P_0_416 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_417 = *+1
 lda #$00
 sta $0D
P_0_418 = *+1
 lda #$00
 sta $0E
P_0_419 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_420 = *+1
 lda #$00
 sta $09
P_0_421 = *+1
 lda #$00
 sta $08
P_0_422 = *+1
 lda #$00
 sta $0D
P_0_423 = *+1
 lda #$00
 sta $0E
P_0_424 = *+1
 lda #$00
 sta $0F
P_0_425 = *+1
 lda #$00
 sta $1B
P_0_426 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_427 = *+1
 lda #$00
 sta $0D
P_0_428 = *+1
 lda #$00
 sta $0E
P_0_429 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_430 = *+1
 lda #$00
 sta $09
P_0_431 = *+1
 lda #$00
 sta $08
P_0_432 = *+1
 lda #$00
 sta $0D
P_0_433 = *+1
 lda #$00
 sta $0E
P_0_434 = *+1
 lda #$00
 sta $0F
P_0_435 = *+1
 lda #$00
 sta $1B
P_0_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_437 = *+1
 lda #$00
 sta $0D
P_0_438 = *+1
 lda #$00
 sta $0E
P_0_439 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_440 = *+1
 lda #$00
 sta $09
P_0_441 = *+1
 lda #$00
 sta $08
P_0_442 = *+1
 lda #$00
 sta $0D
P_0_443 = *+1
 lda #$00
 sta $0E
P_0_444 = *+1
 lda #$00
 sta $0F
P_0_445 = *+1
 lda #$00
 sta $1B
P_0_446 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_447 = *+1
 lda #$00
 sta $0D
P_0_448 = *+1
 lda #$00
 sta $0E
P_0_449 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_450 = *+1
 lda #$00
 sta $09
P_0_451 = *+1
 lda #$00
 sta $08
P_0_452 = *+1
 lda #$00
 sta $0D
P_0_453 = *+1
 lda #$00
 sta $0E
P_0_454 = *+1
 lda #$00
 sta $0F
P_0_455 = *+1
 lda #$00
 sta $1B
P_0_456 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_457 = *+1
 lda #$00
 sta $0D
P_0_458 = *+1
 lda #$00
 sta $0E
P_0_459 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_460 = *+1
 lda #$00
 sta $09
P_0_461 = *+1
 lda #$00
 sta $08
P_0_462 = *+1
 lda #$00
 sta $0D
P_0_463 = *+1
 lda #$00
 sta $0E
P_0_464 = *+1
 lda #$00
 sta $0F
P_0_465 = *+1
 lda #$00
 sta $1B
P_0_466 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_467 = *+1
 lda #$00
 sta $0D
P_0_468 = *+1
 lda #$00
 sta $0E
P_0_469 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_470 = *+1
 lda #$00
 sta $09
P_0_471 = *+1
 lda #$00
 sta $08
P_0_472 = *+1
 lda #$00
 sta $0D
P_0_473 = *+1
 lda #$00
 sta $0E
P_0_474 = *+1
 lda #$00
 sta $0F
P_0_475 = *+1
 lda #$00
 sta $1B
P_0_476 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_477 = *+1
 lda #$00
 sta $0D
P_0_478 = *+1
 lda #$00
 sta $0E
P_0_479 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_480 = *+1
 lda #$00
 sta $09
P_0_481 = *+1
 lda #$00
 sta $08
P_0_482 = *+1
 lda #$00
 sta $0D
P_0_483 = *+1
 lda #$00
 sta $0E
P_0_484 = *+1
 lda #$00
 sta $0F
P_0_485 = *+1
 lda #$00
 sta $1B
P_0_486 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_487 = *+1
 lda #$00
 sta $0D
P_0_488 = *+1
 lda #$00
 sta $0E
P_0_489 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_490 = *+1
 lda #$00
 sta $09
P_0_491 = *+1
 lda #$00
 sta $08
P_0_492 = *+1
 lda #$00
 sta $0D
P_0_493 = *+1
 lda #$00
 sta $0E
P_0_494 = *+1
 lda #$00
 sta $0F
P_0_495 = *+1
 lda #$00
 sta $1B
P_0_496 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_497 = *+1
 lda #$00
 sta $0D
P_0_498 = *+1
 lda #$00
 sta $0E
P_0_499 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_500 = *+1
 lda #$00
 sta $09
P_0_501 = *+1
 lda #$00
 sta $08
P_0_502 = *+1
 lda #$00
 sta $0D
P_0_503 = *+1
 lda #$00
 sta $0E
P_0_504 = *+1
 lda #$00
 sta $0F
P_0_505 = *+1
 lda #$00
 sta $1B
P_0_506 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_507 = *+1
 lda #$00
 sta $0D
P_0_508 = *+1
 lda #$00
 sta $0E
P_0_509 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_510 = *+1
 lda #$00
 sta $09
P_0_511 = *+1
 lda #$00
 sta $08
P_0_512 = *+1
 lda #$00
 sta $0D
P_0_513 = *+1
 lda #$00
 sta $0E
P_0_514 = *+1
 lda #$00
 sta $0F
P_0_515 = *+1
 lda #$00
 sta $1B
P_0_516 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_517 = *+1
 lda #$00
 sta $0D
P_0_518 = *+1
 lda #$00
 sta $0E
P_0_519 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_520 = *+1
 lda #$00
 sta $09
P_0_521 = *+1
 lda #$00
 sta $08
P_0_522 = *+1
 lda #$00
 sta $0D
P_0_523 = *+1
 lda #$00
 sta $0E
P_0_524 = *+1
 lda #$00
 sta $0F
P_0_525 = *+1
 lda #$00
 sta $1B
P_0_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_527 = *+1
 lda #$00
 sta $0D
P_0_528 = *+1
 lda #$00
 sta $0E
P_0_529 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_530 = *+1
 lda #$00
 sta $09
P_0_531 = *+1
 lda #$00
 sta $08
P_0_532 = *+1
 lda #$00
 sta $0D
P_0_533 = *+1
 lda #$00
 sta $0E
P_0_534 = *+1
 lda #$00
 sta $0F
P_0_535 = *+1
 lda #$00
 sta $1B
P_0_536 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_537 = *+1
 lda #$00
 sta $0D
P_0_538 = *+1
 lda #$00
 sta $0E
P_0_539 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_540 = *+1
 lda #$00
 sta $09
P_0_541 = *+1
 lda #$00
 sta $08
P_0_542 = *+1
 lda #$00
 sta $0D
P_0_543 = *+1
 lda #$00
 sta $0E
P_0_544 = *+1
 lda #$00
 sta $0F
P_0_545 = *+1
 lda #$00
 sta $1B
P_0_546 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_547 = *+1
 lda #$00
 sta $0D
P_0_548 = *+1
 lda #$00
 sta $0E
P_0_549 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_550 = *+1
 lda #$00
 sta $09
P_0_551 = *+1
 lda #$00
 sta $08
P_0_552 = *+1
 lda #$00
 sta $0D
P_0_553 = *+1
 lda #$00
 sta $0E
P_0_554 = *+1
 lda #$00
 sta $0F
P_0_555 = *+1
 lda #$00
 sta $1B
P_0_556 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_557 = *+1
 lda #$00
 sta $0D
P_0_558 = *+1
 lda #$00
 sta $0E
P_0_559 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_560 = *+1
 lda #$00
 sta $09
P_0_561 = *+1
 lda #$00
 sta $08
P_0_562 = *+1
 lda #$00
 sta $0D
P_0_563 = *+1
 lda #$00
 sta $0E
P_0_564 = *+1
 lda #$00
 sta $0F
P_0_565 = *+1
 lda #$00
 sta $1B
P_0_566 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_567 = *+1
 lda #$00
 sta $0D
P_0_568 = *+1
 lda #$00
 sta $0E
P_0_569 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_570 = *+1
 lda #$00
 sta $09
P_0_571 = *+1
 lda #$00
 sta $08
P_0_572 = *+1
 lda #$00
 sta $0D
P_0_573 = *+1
 lda #$00
 sta $0E
P_0_574 = *+1
 lda #$00
 sta $0F
P_0_575 = *+1
 lda #$00
 sta $1B
P_0_576 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_577 = *+1
 lda #$00
 sta $0D
P_0_578 = *+1
 lda #$00
 sta $0E
P_0_579 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_580 = *+1
 lda #$00
 sta $09
P_0_581 = *+1
 lda #$00
 sta $08
P_0_582 = *+1
 lda #$00
 sta $0D
P_0_583 = *+1
 lda #$00
 sta $0E
P_0_584 = *+1
 lda #$00
 sta $0F
P_0_585 = *+1
 lda #$00
 sta $1B
P_0_586 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_587 = *+1
 lda #$00
 sta $0D
P_0_588 = *+1
 lda #$00
 sta $0E
P_0_589 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_590 = *+1
 lda #$00
 sta $09
P_0_591 = *+1
 lda #$00
 sta $08
P_0_592 = *+1
 lda #$00
 sta $0D
P_0_593 = *+1
 lda #$00
 sta $0E
P_0_594 = *+1
 lda #$00
 sta $0F
P_0_595 = *+1
 lda #$00
 sta $1B
P_0_596 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_597 = *+1
 lda #$00
 sta $0D
P_0_598 = *+1
 lda #$00
 sta $0E
P_0_599 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_600 = *+1
 lda #$00
 sta $09
P_0_601 = *+1
 lda #$00
 sta $08
P_0_602 = *+1
 lda #$00
 sta $0D
P_0_603 = *+1
 lda #$00
 sta $0E
P_0_604 = *+1
 lda #$00
 sta $0F
P_0_605 = *+1
 lda #$00
 sta $1B
P_0_606 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_607 = *+1
 lda #$00
 sta $0D
P_0_608 = *+1
 lda #$00
 sta $0E
P_0_609 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_610 = *+1
 lda #$00
 sta $09
P_0_611 = *+1
 lda #$00
 sta $08
P_0_612 = *+1
 lda #$00
 sta $0D
P_0_613 = *+1
 lda #$00
 sta $0E
P_0_614 = *+1
 lda #$00
 sta $0F
P_0_615 = *+1
 lda #$00
 sta $1B
P_0_616 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_617 = *+1
 lda #$00
 sta $0D
P_0_618 = *+1
 lda #$00
 sta $0E
P_0_619 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_620 = *+1
 lda #$00
 sta $09
P_0_621 = *+1
 lda #$00
 sta $08
P_0_622 = *+1
 lda #$00
 sta $0D
P_0_623 = *+1
 lda #$00
 sta $0E
P_0_624 = *+1
 lda #$00
 sta $0F
P_0_625 = *+1
 lda #$00
 sta $1B
P_0_626 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_627 = *+1
 lda #$00
 sta $0D
P_0_628 = *+1
 lda #$00
 sta $0E
P_0_629 = *+1
 lda #$00
 sta $0F
 sta $02
P_0_630 = *+1
 lda #$00
 sta $09
P_0_631 = *+1
 lda #$00
 sta $08
P_0_632 = *+1
 lda #$00
 sta $0D
P_0_633 = *+1
 lda #$00
 sta $0E
P_0_634 = *+1
 lda #$00
 sta $0F
P_0_635 = *+1
 lda #$00
 sta $1B
P_0_636 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_0_637 = *+1
 lda #$00
 sta $0D
P_0_638 = *+1
 lda #$00
 sta $0E
P_0_639 = *+1
 lda #$00
 sta $0F
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
 sta $08
P_1_2 = *+1
 lda #$00
 sta $0D
P_1_3 = *+1
 lda #$00
 sta $0E
P_1_4 = *+1
 lda #$00
 sta $0F
P_1_5 = *+1
 lda #$00
 sta $1B
P_1_6 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_7 = *+1
 lda #$00
 sta $0D
P_1_8 = *+1
 lda #$00
 sta $0E
P_1_9 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_10 = *+1
 lda #$00
 sta $09
P_1_11 = *+1
 lda #$00
 sta $08
P_1_12 = *+1
 lda #$00
 sta $0D
P_1_13 = *+1
 lda #$00
 sta $0E
P_1_14 = *+1
 lda #$00
 sta $0F
P_1_15 = *+1
 lda #$00
 sta $1B
P_1_16 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_17 = *+1
 lda #$00
 sta $0D
P_1_18 = *+1
 lda #$00
 sta $0E
P_1_19 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_20 = *+1
 lda #$00
 sta $09
P_1_21 = *+1
 lda #$00
 sta $08
P_1_22 = *+1
 lda #$00
 sta $0D
P_1_23 = *+1
 lda #$00
 sta $0E
P_1_24 = *+1
 lda #$00
 sta $0F
P_1_25 = *+1
 lda #$00
 sta $1B
P_1_26 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_27 = *+1
 lda #$00
 sta $0D
P_1_28 = *+1
 lda #$00
 sta $0E
P_1_29 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_30 = *+1
 lda #$00
 sta $09
P_1_31 = *+1
 lda #$00
 sta $08
P_1_32 = *+1
 lda #$00
 sta $0D
P_1_33 = *+1
 lda #$00
 sta $0E
P_1_34 = *+1
 lda #$00
 sta $0F
P_1_35 = *+1
 lda #$00
 sta $1B
P_1_36 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_37 = *+1
 lda #$00
 sta $0D
P_1_38 = *+1
 lda #$00
 sta $0E
P_1_39 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_40 = *+1
 lda #$00
 sta $09
P_1_41 = *+1
 lda #$00
 sta $08
P_1_42 = *+1
 lda #$00
 sta $0D
P_1_43 = *+1
 lda #$00
 sta $0E
P_1_44 = *+1
 lda #$00
 sta $0F
P_1_45 = *+1
 lda #$00
 sta $1B
P_1_46 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_47 = *+1
 lda #$00
 sta $0D
P_1_48 = *+1
 lda #$00
 sta $0E
P_1_49 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_50 = *+1
 lda #$00
 sta $09
P_1_51 = *+1
 lda #$00
 sta $08
P_1_52 = *+1
 lda #$00
 sta $0D
P_1_53 = *+1
 lda #$00
 sta $0E
P_1_54 = *+1
 lda #$00
 sta $0F
P_1_55 = *+1
 lda #$00
 sta $1B
P_1_56 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_57 = *+1
 lda #$00
 sta $0D
P_1_58 = *+1
 lda #$00
 sta $0E
P_1_59 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_60 = *+1
 lda #$00
 sta $09
P_1_61 = *+1
 lda #$00
 sta $08
P_1_62 = *+1
 lda #$00
 sta $0D
P_1_63 = *+1
 lda #$00
 sta $0E
P_1_64 = *+1
 lda #$00
 sta $0F
P_1_65 = *+1
 lda #$00
 sta $1B
P_1_66 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_67 = *+1
 lda #$00
 sta $0D
P_1_68 = *+1
 lda #$00
 sta $0E
P_1_69 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_70 = *+1
 lda #$00
 sta $09
P_1_71 = *+1
 lda #$00
 sta $08
P_1_72 = *+1
 lda #$00
 sta $0D
P_1_73 = *+1
 lda #$00
 sta $0E
P_1_74 = *+1
 lda #$00
 sta $0F
P_1_75 = *+1
 lda #$00
 sta $1B
P_1_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_77 = *+1
 lda #$00
 sta $0D
P_1_78 = *+1
 lda #$00
 sta $0E
P_1_79 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_80 = *+1
 lda #$00
 sta $09
P_1_81 = *+1
 lda #$00
 sta $08
P_1_82 = *+1
 lda #$00
 sta $0D
P_1_83 = *+1
 lda #$00
 sta $0E
P_1_84 = *+1
 lda #$00
 sta $0F
P_1_85 = *+1
 lda #$00
 sta $1B
P_1_86 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_87 = *+1
 lda #$00
 sta $0D
P_1_88 = *+1
 lda #$00
 sta $0E
P_1_89 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_90 = *+1
 lda #$00
 sta $09
P_1_91 = *+1
 lda #$00
 sta $08
P_1_92 = *+1
 lda #$00
 sta $0D
P_1_93 = *+1
 lda #$00
 sta $0E
P_1_94 = *+1
 lda #$00
 sta $0F
P_1_95 = *+1
 lda #$00
 sta $1B
P_1_96 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_97 = *+1
 lda #$00
 sta $0D
P_1_98 = *+1
 lda #$00
 sta $0E
P_1_99 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_100 = *+1
 lda #$00
 sta $09
P_1_101 = *+1
 lda #$00
 sta $08
P_1_102 = *+1
 lda #$00
 sta $0D
P_1_103 = *+1
 lda #$00
 sta $0E
P_1_104 = *+1
 lda #$00
 sta $0F
P_1_105 = *+1
 lda #$00
 sta $1B
P_1_106 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_107 = *+1
 lda #$00
 sta $0D
P_1_108 = *+1
 lda #$00
 sta $0E
P_1_109 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_110 = *+1
 lda #$00
 sta $09
P_1_111 = *+1
 lda #$00
 sta $08
P_1_112 = *+1
 lda #$00
 sta $0D
P_1_113 = *+1
 lda #$00
 sta $0E
P_1_114 = *+1
 lda #$00
 sta $0F
P_1_115 = *+1
 lda #$00
 sta $1B
P_1_116 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_117 = *+1
 lda #$00
 sta $0D
P_1_118 = *+1
 lda #$00
 sta $0E
P_1_119 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_120 = *+1
 lda #$00
 sta $09
P_1_121 = *+1
 lda #$00
 sta $08
P_1_122 = *+1
 lda #$00
 sta $0D
P_1_123 = *+1
 lda #$00
 sta $0E
P_1_124 = *+1
 lda #$00
 sta $0F
P_1_125 = *+1
 lda #$00
 sta $1B
P_1_126 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_127 = *+1
 lda #$00
 sta $0D
P_1_128 = *+1
 lda #$00
 sta $0E
P_1_129 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_130 = *+1
 lda #$00
 sta $09
P_1_131 = *+1
 lda #$00
 sta $08
P_1_132 = *+1
 lda #$00
 sta $0D
P_1_133 = *+1
 lda #$00
 sta $0E
P_1_134 = *+1
 lda #$00
 sta $0F
P_1_135 = *+1
 lda #$00
 sta $1B
P_1_136 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_137 = *+1
 lda #$00
 sta $0D
P_1_138 = *+1
 lda #$00
 sta $0E
P_1_139 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_140 = *+1
 lda #$00
 sta $09
P_1_141 = *+1
 lda #$00
 sta $08
P_1_142 = *+1
 lda #$00
 sta $0D
P_1_143 = *+1
 lda #$00
 sta $0E
P_1_144 = *+1
 lda #$00
 sta $0F
P_1_145 = *+1
 lda #$00
 sta $1B
P_1_146 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_147 = *+1
 lda #$00
 sta $0D
P_1_148 = *+1
 lda #$00
 sta $0E
P_1_149 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_150 = *+1
 lda #$00
 sta $09
P_1_151 = *+1
 lda #$00
 sta $08
P_1_152 = *+1
 lda #$00
 sta $0D
P_1_153 = *+1
 lda #$00
 sta $0E
P_1_154 = *+1
 lda #$00
 sta $0F
P_1_155 = *+1
 lda #$00
 sta $1B
P_1_156 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_157 = *+1
 lda #$00
 sta $0D
P_1_158 = *+1
 lda #$00
 sta $0E
P_1_159 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_160 = *+1
 lda #$00
 sta $09
P_1_161 = *+1
 lda #$00
 sta $08
P_1_162 = *+1
 lda #$00
 sta $0D
P_1_163 = *+1
 lda #$00
 sta $0E
P_1_164 = *+1
 lda #$00
 sta $0F
P_1_165 = *+1
 lda #$00
 sta $1B
P_1_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_167 = *+1
 lda #$00
 sta $0D
P_1_168 = *+1
 lda #$00
 sta $0E
P_1_169 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_170 = *+1
 lda #$00
 sta $09
P_1_171 = *+1
 lda #$00
 sta $08
P_1_172 = *+1
 lda #$00
 sta $0D
P_1_173 = *+1
 lda #$00
 sta $0E
P_1_174 = *+1
 lda #$00
 sta $0F
P_1_175 = *+1
 lda #$00
 sta $1B
P_1_176 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_177 = *+1
 lda #$00
 sta $0D
P_1_178 = *+1
 lda #$00
 sta $0E
P_1_179 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_180 = *+1
 lda #$00
 sta $09
P_1_181 = *+1
 lda #$00
 sta $08
P_1_182 = *+1
 lda #$00
 sta $0D
P_1_183 = *+1
 lda #$00
 sta $0E
P_1_184 = *+1
 lda #$00
 sta $0F
P_1_185 = *+1
 lda #$00
 sta $1B
P_1_186 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_187 = *+1
 lda #$00
 sta $0D
P_1_188 = *+1
 lda #$00
 sta $0E
P_1_189 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_190 = *+1
 lda #$00
 sta $09
P_1_191 = *+1
 lda #$00
 sta $08
P_1_192 = *+1
 lda #$00
 sta $0D
P_1_193 = *+1
 lda #$00
 sta $0E
P_1_194 = *+1
 lda #$00
 sta $0F
P_1_195 = *+1
 lda #$00
 sta $1B
P_1_196 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_197 = *+1
 lda #$00
 sta $0D
P_1_198 = *+1
 lda #$00
 sta $0E
P_1_199 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_200 = *+1
 lda #$00
 sta $09
P_1_201 = *+1
 lda #$00
 sta $08
P_1_202 = *+1
 lda #$00
 sta $0D
P_1_203 = *+1
 lda #$00
 sta $0E
P_1_204 = *+1
 lda #$00
 sta $0F
P_1_205 = *+1
 lda #$00
 sta $1B
P_1_206 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_207 = *+1
 lda #$00
 sta $0D
P_1_208 = *+1
 lda #$00
 sta $0E
P_1_209 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_210 = *+1
 lda #$00
 sta $09
P_1_211 = *+1
 lda #$00
 sta $08
P_1_212 = *+1
 lda #$00
 sta $0D
P_1_213 = *+1
 lda #$00
 sta $0E
P_1_214 = *+1
 lda #$00
 sta $0F
P_1_215 = *+1
 lda #$00
 sta $1B
P_1_216 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_217 = *+1
 lda #$00
 sta $0D
P_1_218 = *+1
 lda #$00
 sta $0E
P_1_219 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_220 = *+1
 lda #$00
 sta $09
P_1_221 = *+1
 lda #$00
 sta $08
P_1_222 = *+1
 lda #$00
 sta $0D
P_1_223 = *+1
 lda #$00
 sta $0E
P_1_224 = *+1
 lda #$00
 sta $0F
P_1_225 = *+1
 lda #$00
 sta $1B
P_1_226 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_227 = *+1
 lda #$00
 sta $0D
P_1_228 = *+1
 lda #$00
 sta $0E
P_1_229 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_230 = *+1
 lda #$00
 sta $09
P_1_231 = *+1
 lda #$00
 sta $08
P_1_232 = *+1
 lda #$00
 sta $0D
P_1_233 = *+1
 lda #$00
 sta $0E
P_1_234 = *+1
 lda #$00
 sta $0F
P_1_235 = *+1
 lda #$00
 sta $1B
P_1_236 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_237 = *+1
 lda #$00
 sta $0D
P_1_238 = *+1
 lda #$00
 sta $0E
P_1_239 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_240 = *+1
 lda #$00
 sta $09
P_1_241 = *+1
 lda #$00
 sta $08
P_1_242 = *+1
 lda #$00
 sta $0D
P_1_243 = *+1
 lda #$00
 sta $0E
P_1_244 = *+1
 lda #$00
 sta $0F
P_1_245 = *+1
 lda #$00
 sta $1B
P_1_246 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_247 = *+1
 lda #$00
 sta $0D
P_1_248 = *+1
 lda #$00
 sta $0E
P_1_249 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_250 = *+1
 lda #$00
 sta $09
P_1_251 = *+1
 lda #$00
 sta $08
P_1_252 = *+1
 lda #$00
 sta $0D
P_1_253 = *+1
 lda #$00
 sta $0E
P_1_254 = *+1
 lda #$00
 sta $0F
P_1_255 = *+1
 lda #$00
 sta $1B
P_1_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_257 = *+1
 lda #$00
 sta $0D
P_1_258 = *+1
 lda #$00
 sta $0E
P_1_259 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_260 = *+1
 lda #$00
 sta $09
P_1_261 = *+1
 lda #$00
 sta $08
P_1_262 = *+1
 lda #$00
 sta $0D
P_1_263 = *+1
 lda #$00
 sta $0E
P_1_264 = *+1
 lda #$00
 sta $0F
P_1_265 = *+1
 lda #$00
 sta $1B
P_1_266 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_267 = *+1
 lda #$00
 sta $0D
P_1_268 = *+1
 lda #$00
 sta $0E
P_1_269 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_270 = *+1
 lda #$00
 sta $09
P_1_271 = *+1
 lda #$00
 sta $08
P_1_272 = *+1
 lda #$00
 sta $0D
P_1_273 = *+1
 lda #$00
 sta $0E
P_1_274 = *+1
 lda #$00
 sta $0F
P_1_275 = *+1
 lda #$00
 sta $1B
P_1_276 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_277 = *+1
 lda #$00
 sta $0D
P_1_278 = *+1
 lda #$00
 sta $0E
P_1_279 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_280 = *+1
 lda #$00
 sta $09
P_1_281 = *+1
 lda #$00
 sta $08
P_1_282 = *+1
 lda #$00
 sta $0D
P_1_283 = *+1
 lda #$00
 sta $0E
P_1_284 = *+1
 lda #$00
 sta $0F
P_1_285 = *+1
 lda #$00
 sta $1B
P_1_286 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_287 = *+1
 lda #$00
 sta $0D
P_1_288 = *+1
 lda #$00
 sta $0E
P_1_289 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_290 = *+1
 lda #$00
 sta $09
P_1_291 = *+1
 lda #$00
 sta $08
P_1_292 = *+1
 lda #$00
 sta $0D
P_1_293 = *+1
 lda #$00
 sta $0E
P_1_294 = *+1
 lda #$00
 sta $0F
P_1_295 = *+1
 lda #$00
 sta $1B
P_1_296 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_297 = *+1
 lda #$00
 sta $0D
P_1_298 = *+1
 lda #$00
 sta $0E
P_1_299 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_300 = *+1
 lda #$00
 sta $09
P_1_301 = *+1
 lda #$00
 sta $08
P_1_302 = *+1
 lda #$00
 sta $0D
P_1_303 = *+1
 lda #$00
 sta $0E
P_1_304 = *+1
 lda #$00
 sta $0F
P_1_305 = *+1
 lda #$00
 sta $1B
P_1_306 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_307 = *+1
 lda #$00
 sta $0D
P_1_308 = *+1
 lda #$00
 sta $0E
P_1_309 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_310 = *+1
 lda #$00
 sta $09
P_1_311 = *+1
 lda #$00
 sta $08
P_1_312 = *+1
 lda #$00
 sta $0D
P_1_313 = *+1
 lda #$00
 sta $0E
P_1_314 = *+1
 lda #$00
 sta $0F
P_1_315 = *+1
 lda #$00
 sta $1B
P_1_316 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_317 = *+1
 lda #$00
 sta $0D
P_1_318 = *+1
 lda #$00
 sta $0E
P_1_319 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_320 = *+1
 lda #$00
 sta $09
P_1_321 = *+1
 lda #$00
 sta $08
P_1_322 = *+1
 lda #$00
 sta $0D
P_1_323 = *+1
 lda #$00
 sta $0E
P_1_324 = *+1
 lda #$00
 sta $0F
P_1_325 = *+1
 lda #$00
 sta $1B
P_1_326 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_327 = *+1
 lda #$00
 sta $0D
P_1_328 = *+1
 lda #$00
 sta $0E
P_1_329 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_330 = *+1
 lda #$00
 sta $09
P_1_331 = *+1
 lda #$00
 sta $08
P_1_332 = *+1
 lda #$00
 sta $0D
P_1_333 = *+1
 lda #$00
 sta $0E
P_1_334 = *+1
 lda #$00
 sta $0F
P_1_335 = *+1
 lda #$00
 sta $1B
P_1_336 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_337 = *+1
 lda #$00
 sta $0D
P_1_338 = *+1
 lda #$00
 sta $0E
P_1_339 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_340 = *+1
 lda #$00
 sta $09
P_1_341 = *+1
 lda #$00
 sta $08
P_1_342 = *+1
 lda #$00
 sta $0D
P_1_343 = *+1
 lda #$00
 sta $0E
P_1_344 = *+1
 lda #$00
 sta $0F
P_1_345 = *+1
 lda #$00
 sta $1B
P_1_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_347 = *+1
 lda #$00
 sta $0D
P_1_348 = *+1
 lda #$00
 sta $0E
P_1_349 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_350 = *+1
 lda #$00
 sta $09
P_1_351 = *+1
 lda #$00
 sta $08
P_1_352 = *+1
 lda #$00
 sta $0D
P_1_353 = *+1
 lda #$00
 sta $0E
P_1_354 = *+1
 lda #$00
 sta $0F
P_1_355 = *+1
 lda #$00
 sta $1B
P_1_356 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_357 = *+1
 lda #$00
 sta $0D
P_1_358 = *+1
 lda #$00
 sta $0E
P_1_359 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_360 = *+1
 lda #$00
 sta $09
P_1_361 = *+1
 lda #$00
 sta $08
P_1_362 = *+1
 lda #$00
 sta $0D
P_1_363 = *+1
 lda #$00
 sta $0E
P_1_364 = *+1
 lda #$00
 sta $0F
P_1_365 = *+1
 lda #$00
 sta $1B
P_1_366 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_367 = *+1
 lda #$00
 sta $0D
P_1_368 = *+1
 lda #$00
 sta $0E
P_1_369 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_370 = *+1
 lda #$00
 sta $09
P_1_371 = *+1
 lda #$00
 sta $08
P_1_372 = *+1
 lda #$00
 sta $0D
P_1_373 = *+1
 lda #$00
 sta $0E
P_1_374 = *+1
 lda #$00
 sta $0F
P_1_375 = *+1
 lda #$00
 sta $1B
P_1_376 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_377 = *+1
 lda #$00
 sta $0D
P_1_378 = *+1
 lda #$00
 sta $0E
P_1_379 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_380 = *+1
 lda #$00
 sta $09
P_1_381 = *+1
 lda #$00
 sta $08
P_1_382 = *+1
 lda #$00
 sta $0D
P_1_383 = *+1
 lda #$00
 sta $0E
P_1_384 = *+1
 lda #$00
 sta $0F
P_1_385 = *+1
 lda #$00
 sta $1B
P_1_386 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_387 = *+1
 lda #$00
 sta $0D
P_1_388 = *+1
 lda #$00
 sta $0E
P_1_389 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_390 = *+1
 lda #$00
 sta $09
P_1_391 = *+1
 lda #$00
 sta $08
P_1_392 = *+1
 lda #$00
 sta $0D
P_1_393 = *+1
 lda #$00
 sta $0E
P_1_394 = *+1
 lda #$00
 sta $0F
P_1_395 = *+1
 lda #$00
 sta $1B
P_1_396 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_397 = *+1
 lda #$00
 sta $0D
P_1_398 = *+1
 lda #$00
 sta $0E
P_1_399 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_400 = *+1
 lda #$00
 sta $09
P_1_401 = *+1
 lda #$00
 sta $08
P_1_402 = *+1
 lda #$00
 sta $0D
P_1_403 = *+1
 lda #$00
 sta $0E
P_1_404 = *+1
 lda #$00
 sta $0F
P_1_405 = *+1
 lda #$00
 sta $1B
P_1_406 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_407 = *+1
 lda #$00
 sta $0D
P_1_408 = *+1
 lda #$00
 sta $0E
P_1_409 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_410 = *+1
 lda #$00
 sta $09
P_1_411 = *+1
 lda #$00
 sta $08
P_1_412 = *+1
 lda #$00
 sta $0D
P_1_413 = *+1
 lda #$00
 sta $0E
P_1_414 = *+1
 lda #$00
 sta $0F
P_1_415 = *+1
 lda #$00
 sta $1B
P_1_416 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_417 = *+1
 lda #$00
 sta $0D
P_1_418 = *+1
 lda #$00
 sta $0E
P_1_419 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_420 = *+1
 lda #$00
 sta $09
P_1_421 = *+1
 lda #$00
 sta $08
P_1_422 = *+1
 lda #$00
 sta $0D
P_1_423 = *+1
 lda #$00
 sta $0E
P_1_424 = *+1
 lda #$00
 sta $0F
P_1_425 = *+1
 lda #$00
 sta $1B
P_1_426 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_427 = *+1
 lda #$00
 sta $0D
P_1_428 = *+1
 lda #$00
 sta $0E
P_1_429 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_430 = *+1
 lda #$00
 sta $09
P_1_431 = *+1
 lda #$00
 sta $08
P_1_432 = *+1
 lda #$00
 sta $0D
P_1_433 = *+1
 lda #$00
 sta $0E
P_1_434 = *+1
 lda #$00
 sta $0F
P_1_435 = *+1
 lda #$00
 sta $1B
P_1_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_437 = *+1
 lda #$00
 sta $0D
P_1_438 = *+1
 lda #$00
 sta $0E
P_1_439 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_440 = *+1
 lda #$00
 sta $09
P_1_441 = *+1
 lda #$00
 sta $08
P_1_442 = *+1
 lda #$00
 sta $0D
P_1_443 = *+1
 lda #$00
 sta $0E
P_1_444 = *+1
 lda #$00
 sta $0F
P_1_445 = *+1
 lda #$00
 sta $1B
P_1_446 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_447 = *+1
 lda #$00
 sta $0D
P_1_448 = *+1
 lda #$00
 sta $0E
P_1_449 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_450 = *+1
 lda #$00
 sta $09
P_1_451 = *+1
 lda #$00
 sta $08
P_1_452 = *+1
 lda #$00
 sta $0D
P_1_453 = *+1
 lda #$00
 sta $0E
P_1_454 = *+1
 lda #$00
 sta $0F
P_1_455 = *+1
 lda #$00
 sta $1B
P_1_456 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_457 = *+1
 lda #$00
 sta $0D
P_1_458 = *+1
 lda #$00
 sta $0E
P_1_459 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_460 = *+1
 lda #$00
 sta $09
P_1_461 = *+1
 lda #$00
 sta $08
P_1_462 = *+1
 lda #$00
 sta $0D
P_1_463 = *+1
 lda #$00
 sta $0E
P_1_464 = *+1
 lda #$00
 sta $0F
P_1_465 = *+1
 lda #$00
 sta $1B
P_1_466 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_467 = *+1
 lda #$00
 sta $0D
P_1_468 = *+1
 lda #$00
 sta $0E
P_1_469 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_470 = *+1
 lda #$00
 sta $09
P_1_471 = *+1
 lda #$00
 sta $08
P_1_472 = *+1
 lda #$00
 sta $0D
P_1_473 = *+1
 lda #$00
 sta $0E
P_1_474 = *+1
 lda #$00
 sta $0F
P_1_475 = *+1
 lda #$00
 sta $1B
P_1_476 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_477 = *+1
 lda #$00
 sta $0D
P_1_478 = *+1
 lda #$00
 sta $0E
P_1_479 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_480 = *+1
 lda #$00
 sta $09
P_1_481 = *+1
 lda #$00
 sta $08
P_1_482 = *+1
 lda #$00
 sta $0D
P_1_483 = *+1
 lda #$00
 sta $0E
P_1_484 = *+1
 lda #$00
 sta $0F
P_1_485 = *+1
 lda #$00
 sta $1B
P_1_486 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_487 = *+1
 lda #$00
 sta $0D
P_1_488 = *+1
 lda #$00
 sta $0E
P_1_489 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_490 = *+1
 lda #$00
 sta $09
P_1_491 = *+1
 lda #$00
 sta $08
P_1_492 = *+1
 lda #$00
 sta $0D
P_1_493 = *+1
 lda #$00
 sta $0E
P_1_494 = *+1
 lda #$00
 sta $0F
P_1_495 = *+1
 lda #$00
 sta $1B
P_1_496 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_497 = *+1
 lda #$00
 sta $0D
P_1_498 = *+1
 lda #$00
 sta $0E
P_1_499 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_500 = *+1
 lda #$00
 sta $09
P_1_501 = *+1
 lda #$00
 sta $08
P_1_502 = *+1
 lda #$00
 sta $0D
P_1_503 = *+1
 lda #$00
 sta $0E
P_1_504 = *+1
 lda #$00
 sta $0F
P_1_505 = *+1
 lda #$00
 sta $1B
P_1_506 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_507 = *+1
 lda #$00
 sta $0D
P_1_508 = *+1
 lda #$00
 sta $0E
P_1_509 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_510 = *+1
 lda #$00
 sta $09
P_1_511 = *+1
 lda #$00
 sta $08
P_1_512 = *+1
 lda #$00
 sta $0D
P_1_513 = *+1
 lda #$00
 sta $0E
P_1_514 = *+1
 lda #$00
 sta $0F
P_1_515 = *+1
 lda #$00
 sta $1B
P_1_516 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_517 = *+1
 lda #$00
 sta $0D
P_1_518 = *+1
 lda #$00
 sta $0E
P_1_519 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_520 = *+1
 lda #$00
 sta $09
P_1_521 = *+1
 lda #$00
 sta $08
P_1_522 = *+1
 lda #$00
 sta $0D
P_1_523 = *+1
 lda #$00
 sta $0E
P_1_524 = *+1
 lda #$00
 sta $0F
P_1_525 = *+1
 lda #$00
 sta $1B
P_1_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_527 = *+1
 lda #$00
 sta $0D
P_1_528 = *+1
 lda #$00
 sta $0E
P_1_529 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_530 = *+1
 lda #$00
 sta $09
P_1_531 = *+1
 lda #$00
 sta $08
P_1_532 = *+1
 lda #$00
 sta $0D
P_1_533 = *+1
 lda #$00
 sta $0E
P_1_534 = *+1
 lda #$00
 sta $0F
P_1_535 = *+1
 lda #$00
 sta $1B
P_1_536 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_537 = *+1
 lda #$00
 sta $0D
P_1_538 = *+1
 lda #$00
 sta $0E
P_1_539 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_540 = *+1
 lda #$00
 sta $09
P_1_541 = *+1
 lda #$00
 sta $08
P_1_542 = *+1
 lda #$00
 sta $0D
P_1_543 = *+1
 lda #$00
 sta $0E
P_1_544 = *+1
 lda #$00
 sta $0F
P_1_545 = *+1
 lda #$00
 sta $1B
P_1_546 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_547 = *+1
 lda #$00
 sta $0D
P_1_548 = *+1
 lda #$00
 sta $0E
P_1_549 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_550 = *+1
 lda #$00
 sta $09
P_1_551 = *+1
 lda #$00
 sta $08
P_1_552 = *+1
 lda #$00
 sta $0D
P_1_553 = *+1
 lda #$00
 sta $0E
P_1_554 = *+1
 lda #$00
 sta $0F
P_1_555 = *+1
 lda #$00
 sta $1B
P_1_556 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_557 = *+1
 lda #$00
 sta $0D
P_1_558 = *+1
 lda #$00
 sta $0E
P_1_559 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_560 = *+1
 lda #$00
 sta $09
P_1_561 = *+1
 lda #$00
 sta $08
P_1_562 = *+1
 lda #$00
 sta $0D
P_1_563 = *+1
 lda #$00
 sta $0E
P_1_564 = *+1
 lda #$00
 sta $0F
P_1_565 = *+1
 lda #$00
 sta $1B
P_1_566 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_567 = *+1
 lda #$00
 sta $0D
P_1_568 = *+1
 lda #$00
 sta $0E
P_1_569 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_570 = *+1
 lda #$00
 sta $09
P_1_571 = *+1
 lda #$00
 sta $08
P_1_572 = *+1
 lda #$00
 sta $0D
P_1_573 = *+1
 lda #$00
 sta $0E
P_1_574 = *+1
 lda #$00
 sta $0F
P_1_575 = *+1
 lda #$00
 sta $1B
P_1_576 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_577 = *+1
 lda #$00
 sta $0D
P_1_578 = *+1
 lda #$00
 sta $0E
P_1_579 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_580 = *+1
 lda #$00
 sta $09
P_1_581 = *+1
 lda #$00
 sta $08
P_1_582 = *+1
 lda #$00
 sta $0D
P_1_583 = *+1
 lda #$00
 sta $0E
P_1_584 = *+1
 lda #$00
 sta $0F
P_1_585 = *+1
 lda #$00
 sta $1B
P_1_586 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_587 = *+1
 lda #$00
 sta $0D
P_1_588 = *+1
 lda #$00
 sta $0E
P_1_589 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_590 = *+1
 lda #$00
 sta $09
P_1_591 = *+1
 lda #$00
 sta $08
P_1_592 = *+1
 lda #$00
 sta $0D
P_1_593 = *+1
 lda #$00
 sta $0E
P_1_594 = *+1
 lda #$00
 sta $0F
P_1_595 = *+1
 lda #$00
 sta $1B
P_1_596 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_597 = *+1
 lda #$00
 sta $0D
P_1_598 = *+1
 lda #$00
 sta $0E
P_1_599 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_600 = *+1
 lda #$00
 sta $09
P_1_601 = *+1
 lda #$00
 sta $08
P_1_602 = *+1
 lda #$00
 sta $0D
P_1_603 = *+1
 lda #$00
 sta $0E
P_1_604 = *+1
 lda #$00
 sta $0F
P_1_605 = *+1
 lda #$00
 sta $1B
P_1_606 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_607 = *+1
 lda #$00
 sta $0D
P_1_608 = *+1
 lda #$00
 sta $0E
P_1_609 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_610 = *+1
 lda #$00
 sta $09
P_1_611 = *+1
 lda #$00
 sta $08
P_1_612 = *+1
 lda #$00
 sta $0D
P_1_613 = *+1
 lda #$00
 sta $0E
P_1_614 = *+1
 lda #$00
 sta $0F
P_1_615 = *+1
 lda #$00
 sta $1B
P_1_616 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_617 = *+1
 lda #$00
 sta $0D
P_1_618 = *+1
 lda #$00
 sta $0E
P_1_619 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_620 = *+1
 lda #$00
 sta $09
P_1_621 = *+1
 lda #$00
 sta $08
P_1_622 = *+1
 lda #$00
 sta $0D
P_1_623 = *+1
 lda #$00
 sta $0E
P_1_624 = *+1
 lda #$00
 sta $0F
P_1_625 = *+1
 lda #$00
 sta $1B
P_1_626 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_627 = *+1
 lda #$00
 sta $0D
P_1_628 = *+1
 lda #$00
 sta $0E
P_1_629 = *+1
 lda #$00
 sta $0F
 sta $02
P_1_630 = *+1
 lda #$00
 sta $09
P_1_631 = *+1
 lda #$00
 sta $08
P_1_632 = *+1
 lda #$00
 sta $0D
P_1_633 = *+1
 lda #$00
 sta $0E
P_1_634 = *+1
 lda #$00
 sta $0F
P_1_635 = *+1
 lda #$00
 sta $1B
P_1_636 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_1_637 = *+1
 lda #$00
 sta $0D
P_1_638 = *+1
 lda #$00
 sta $0E
P_1_639 = *+1
 lda #$00
 sta $0F
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
 sta $08
P_2_2 = *+1
 lda #$00
 sta $0D
P_2_3 = *+1
 lda #$00
 sta $0E
P_2_4 = *+1
 lda #$00
 sta $0F
P_2_5 = *+1
 lda #$00
 sta $1B
P_2_6 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_7 = *+1
 lda #$00
 sta $0D
P_2_8 = *+1
 lda #$00
 sta $0E
P_2_9 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_10 = *+1
 lda #$00
 sta $09
P_2_11 = *+1
 lda #$00
 sta $08
P_2_12 = *+1
 lda #$00
 sta $0D
P_2_13 = *+1
 lda #$00
 sta $0E
P_2_14 = *+1
 lda #$00
 sta $0F
P_2_15 = *+1
 lda #$00
 sta $1B
P_2_16 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_17 = *+1
 lda #$00
 sta $0D
P_2_18 = *+1
 lda #$00
 sta $0E
P_2_19 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_20 = *+1
 lda #$00
 sta $09
P_2_21 = *+1
 lda #$00
 sta $08
P_2_22 = *+1
 lda #$00
 sta $0D
P_2_23 = *+1
 lda #$00
 sta $0E
P_2_24 = *+1
 lda #$00
 sta $0F
P_2_25 = *+1
 lda #$00
 sta $1B
P_2_26 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_27 = *+1
 lda #$00
 sta $0D
P_2_28 = *+1
 lda #$00
 sta $0E
P_2_29 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_30 = *+1
 lda #$00
 sta $09
P_2_31 = *+1
 lda #$00
 sta $08
P_2_32 = *+1
 lda #$00
 sta $0D
P_2_33 = *+1
 lda #$00
 sta $0E
P_2_34 = *+1
 lda #$00
 sta $0F
P_2_35 = *+1
 lda #$00
 sta $1B
P_2_36 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_37 = *+1
 lda #$00
 sta $0D
P_2_38 = *+1
 lda #$00
 sta $0E
P_2_39 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_40 = *+1
 lda #$00
 sta $09
P_2_41 = *+1
 lda #$00
 sta $08
P_2_42 = *+1
 lda #$00
 sta $0D
P_2_43 = *+1
 lda #$00
 sta $0E
P_2_44 = *+1
 lda #$00
 sta $0F
P_2_45 = *+1
 lda #$00
 sta $1B
P_2_46 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_47 = *+1
 lda #$00
 sta $0D
P_2_48 = *+1
 lda #$00
 sta $0E
P_2_49 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_50 = *+1
 lda #$00
 sta $09
P_2_51 = *+1
 lda #$00
 sta $08
P_2_52 = *+1
 lda #$00
 sta $0D
P_2_53 = *+1
 lda #$00
 sta $0E
P_2_54 = *+1
 lda #$00
 sta $0F
P_2_55 = *+1
 lda #$00
 sta $1B
P_2_56 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_57 = *+1
 lda #$00
 sta $0D
P_2_58 = *+1
 lda #$00
 sta $0E
P_2_59 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_60 = *+1
 lda #$00
 sta $09
P_2_61 = *+1
 lda #$00
 sta $08
P_2_62 = *+1
 lda #$00
 sta $0D
P_2_63 = *+1
 lda #$00
 sta $0E
P_2_64 = *+1
 lda #$00
 sta $0F
P_2_65 = *+1
 lda #$00
 sta $1B
P_2_66 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_67 = *+1
 lda #$00
 sta $0D
P_2_68 = *+1
 lda #$00
 sta $0E
P_2_69 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_70 = *+1
 lda #$00
 sta $09
P_2_71 = *+1
 lda #$00
 sta $08
P_2_72 = *+1
 lda #$00
 sta $0D
P_2_73 = *+1
 lda #$00
 sta $0E
P_2_74 = *+1
 lda #$00
 sta $0F
P_2_75 = *+1
 lda #$00
 sta $1B
P_2_76 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_77 = *+1
 lda #$00
 sta $0D
P_2_78 = *+1
 lda #$00
 sta $0E
P_2_79 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_80 = *+1
 lda #$00
 sta $09
P_2_81 = *+1
 lda #$00
 sta $08
P_2_82 = *+1
 lda #$00
 sta $0D
P_2_83 = *+1
 lda #$00
 sta $0E
P_2_84 = *+1
 lda #$00
 sta $0F
P_2_85 = *+1
 lda #$00
 sta $1B
P_2_86 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_87 = *+1
 lda #$00
 sta $0D
P_2_88 = *+1
 lda #$00
 sta $0E
P_2_89 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_90 = *+1
 lda #$00
 sta $09
P_2_91 = *+1
 lda #$00
 sta $08
P_2_92 = *+1
 lda #$00
 sta $0D
P_2_93 = *+1
 lda #$00
 sta $0E
P_2_94 = *+1
 lda #$00
 sta $0F
P_2_95 = *+1
 lda #$00
 sta $1B
P_2_96 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_97 = *+1
 lda #$00
 sta $0D
P_2_98 = *+1
 lda #$00
 sta $0E
P_2_99 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_100 = *+1
 lda #$00
 sta $09
P_2_101 = *+1
 lda #$00
 sta $08
P_2_102 = *+1
 lda #$00
 sta $0D
P_2_103 = *+1
 lda #$00
 sta $0E
P_2_104 = *+1
 lda #$00
 sta $0F
P_2_105 = *+1
 lda #$00
 sta $1B
P_2_106 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_107 = *+1
 lda #$00
 sta $0D
P_2_108 = *+1
 lda #$00
 sta $0E
P_2_109 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_110 = *+1
 lda #$00
 sta $09
P_2_111 = *+1
 lda #$00
 sta $08
P_2_112 = *+1
 lda #$00
 sta $0D
P_2_113 = *+1
 lda #$00
 sta $0E
P_2_114 = *+1
 lda #$00
 sta $0F
P_2_115 = *+1
 lda #$00
 sta $1B
P_2_116 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_117 = *+1
 lda #$00
 sta $0D
P_2_118 = *+1
 lda #$00
 sta $0E
P_2_119 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_120 = *+1
 lda #$00
 sta $09
P_2_121 = *+1
 lda #$00
 sta $08
P_2_122 = *+1
 lda #$00
 sta $0D
P_2_123 = *+1
 lda #$00
 sta $0E
P_2_124 = *+1
 lda #$00
 sta $0F
P_2_125 = *+1
 lda #$00
 sta $1B
P_2_126 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_127 = *+1
 lda #$00
 sta $0D
P_2_128 = *+1
 lda #$00
 sta $0E
P_2_129 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_130 = *+1
 lda #$00
 sta $09
P_2_131 = *+1
 lda #$00
 sta $08
P_2_132 = *+1
 lda #$00
 sta $0D
P_2_133 = *+1
 lda #$00
 sta $0E
P_2_134 = *+1
 lda #$00
 sta $0F
P_2_135 = *+1
 lda #$00
 sta $1B
P_2_136 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_137 = *+1
 lda #$00
 sta $0D
P_2_138 = *+1
 lda #$00
 sta $0E
P_2_139 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_140 = *+1
 lda #$00
 sta $09
P_2_141 = *+1
 lda #$00
 sta $08
P_2_142 = *+1
 lda #$00
 sta $0D
P_2_143 = *+1
 lda #$00
 sta $0E
P_2_144 = *+1
 lda #$00
 sta $0F
P_2_145 = *+1
 lda #$00
 sta $1B
P_2_146 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_147 = *+1
 lda #$00
 sta $0D
P_2_148 = *+1
 lda #$00
 sta $0E
P_2_149 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_150 = *+1
 lda #$00
 sta $09
P_2_151 = *+1
 lda #$00
 sta $08
P_2_152 = *+1
 lda #$00
 sta $0D
P_2_153 = *+1
 lda #$00
 sta $0E
P_2_154 = *+1
 lda #$00
 sta $0F
P_2_155 = *+1
 lda #$00
 sta $1B
P_2_156 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_157 = *+1
 lda #$00
 sta $0D
P_2_158 = *+1
 lda #$00
 sta $0E
P_2_159 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_160 = *+1
 lda #$00
 sta $09
P_2_161 = *+1
 lda #$00
 sta $08
P_2_162 = *+1
 lda #$00
 sta $0D
P_2_163 = *+1
 lda #$00
 sta $0E
P_2_164 = *+1
 lda #$00
 sta $0F
P_2_165 = *+1
 lda #$00
 sta $1B
P_2_166 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_167 = *+1
 lda #$00
 sta $0D
P_2_168 = *+1
 lda #$00
 sta $0E
P_2_169 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_170 = *+1
 lda #$00
 sta $09
P_2_171 = *+1
 lda #$00
 sta $08
P_2_172 = *+1
 lda #$00
 sta $0D
P_2_173 = *+1
 lda #$00
 sta $0E
P_2_174 = *+1
 lda #$00
 sta $0F
P_2_175 = *+1
 lda #$00
 sta $1B
P_2_176 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_177 = *+1
 lda #$00
 sta $0D
P_2_178 = *+1
 lda #$00
 sta $0E
P_2_179 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_180 = *+1
 lda #$00
 sta $09
P_2_181 = *+1
 lda #$00
 sta $08
P_2_182 = *+1
 lda #$00
 sta $0D
P_2_183 = *+1
 lda #$00
 sta $0E
P_2_184 = *+1
 lda #$00
 sta $0F
P_2_185 = *+1
 lda #$00
 sta $1B
P_2_186 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_187 = *+1
 lda #$00
 sta $0D
P_2_188 = *+1
 lda #$00
 sta $0E
P_2_189 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_190 = *+1
 lda #$00
 sta $09
P_2_191 = *+1
 lda #$00
 sta $08
P_2_192 = *+1
 lda #$00
 sta $0D
P_2_193 = *+1
 lda #$00
 sta $0E
P_2_194 = *+1
 lda #$00
 sta $0F
P_2_195 = *+1
 lda #$00
 sta $1B
P_2_196 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_197 = *+1
 lda #$00
 sta $0D
P_2_198 = *+1
 lda #$00
 sta $0E
P_2_199 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_200 = *+1
 lda #$00
 sta $09
P_2_201 = *+1
 lda #$00
 sta $08
P_2_202 = *+1
 lda #$00
 sta $0D
P_2_203 = *+1
 lda #$00
 sta $0E
P_2_204 = *+1
 lda #$00
 sta $0F
P_2_205 = *+1
 lda #$00
 sta $1B
P_2_206 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_207 = *+1
 lda #$00
 sta $0D
P_2_208 = *+1
 lda #$00
 sta $0E
P_2_209 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_210 = *+1
 lda #$00
 sta $09
P_2_211 = *+1
 lda #$00
 sta $08
P_2_212 = *+1
 lda #$00
 sta $0D
P_2_213 = *+1
 lda #$00
 sta $0E
P_2_214 = *+1
 lda #$00
 sta $0F
P_2_215 = *+1
 lda #$00
 sta $1B
P_2_216 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_217 = *+1
 lda #$00
 sta $0D
P_2_218 = *+1
 lda #$00
 sta $0E
P_2_219 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_220 = *+1
 lda #$00
 sta $09
P_2_221 = *+1
 lda #$00
 sta $08
P_2_222 = *+1
 lda #$00
 sta $0D
P_2_223 = *+1
 lda #$00
 sta $0E
P_2_224 = *+1
 lda #$00
 sta $0F
P_2_225 = *+1
 lda #$00
 sta $1B
P_2_226 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_227 = *+1
 lda #$00
 sta $0D
P_2_228 = *+1
 lda #$00
 sta $0E
P_2_229 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_230 = *+1
 lda #$00
 sta $09
P_2_231 = *+1
 lda #$00
 sta $08
P_2_232 = *+1
 lda #$00
 sta $0D
P_2_233 = *+1
 lda #$00
 sta $0E
P_2_234 = *+1
 lda #$00
 sta $0F
P_2_235 = *+1
 lda #$00
 sta $1B
P_2_236 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_237 = *+1
 lda #$00
 sta $0D
P_2_238 = *+1
 lda #$00
 sta $0E
P_2_239 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_240 = *+1
 lda #$00
 sta $09
P_2_241 = *+1
 lda #$00
 sta $08
P_2_242 = *+1
 lda #$00
 sta $0D
P_2_243 = *+1
 lda #$00
 sta $0E
P_2_244 = *+1
 lda #$00
 sta $0F
P_2_245 = *+1
 lda #$00
 sta $1B
P_2_246 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_247 = *+1
 lda #$00
 sta $0D
P_2_248 = *+1
 lda #$00
 sta $0E
P_2_249 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_250 = *+1
 lda #$00
 sta $09
P_2_251 = *+1
 lda #$00
 sta $08
P_2_252 = *+1
 lda #$00
 sta $0D
P_2_253 = *+1
 lda #$00
 sta $0E
P_2_254 = *+1
 lda #$00
 sta $0F
P_2_255 = *+1
 lda #$00
 sta $1B
P_2_256 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_257 = *+1
 lda #$00
 sta $0D
P_2_258 = *+1
 lda #$00
 sta $0E
P_2_259 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_260 = *+1
 lda #$00
 sta $09
P_2_261 = *+1
 lda #$00
 sta $08
P_2_262 = *+1
 lda #$00
 sta $0D
P_2_263 = *+1
 lda #$00
 sta $0E
P_2_264 = *+1
 lda #$00
 sta $0F
P_2_265 = *+1
 lda #$00
 sta $1B
P_2_266 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_267 = *+1
 lda #$00
 sta $0D
P_2_268 = *+1
 lda #$00
 sta $0E
P_2_269 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_270 = *+1
 lda #$00
 sta $09
P_2_271 = *+1
 lda #$00
 sta $08
P_2_272 = *+1
 lda #$00
 sta $0D
P_2_273 = *+1
 lda #$00
 sta $0E
P_2_274 = *+1
 lda #$00
 sta $0F
P_2_275 = *+1
 lda #$00
 sta $1B
P_2_276 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_277 = *+1
 lda #$00
 sta $0D
P_2_278 = *+1
 lda #$00
 sta $0E
P_2_279 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_280 = *+1
 lda #$00
 sta $09
P_2_281 = *+1
 lda #$00
 sta $08
P_2_282 = *+1
 lda #$00
 sta $0D
P_2_283 = *+1
 lda #$00
 sta $0E
P_2_284 = *+1
 lda #$00
 sta $0F
P_2_285 = *+1
 lda #$00
 sta $1B
P_2_286 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_287 = *+1
 lda #$00
 sta $0D
P_2_288 = *+1
 lda #$00
 sta $0E
P_2_289 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_290 = *+1
 lda #$00
 sta $09
P_2_291 = *+1
 lda #$00
 sta $08
P_2_292 = *+1
 lda #$00
 sta $0D
P_2_293 = *+1
 lda #$00
 sta $0E
P_2_294 = *+1
 lda #$00
 sta $0F
P_2_295 = *+1
 lda #$00
 sta $1B
P_2_296 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_297 = *+1
 lda #$00
 sta $0D
P_2_298 = *+1
 lda #$00
 sta $0E
P_2_299 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_300 = *+1
 lda #$00
 sta $09
P_2_301 = *+1
 lda #$00
 sta $08
P_2_302 = *+1
 lda #$00
 sta $0D
P_2_303 = *+1
 lda #$00
 sta $0E
P_2_304 = *+1
 lda #$00
 sta $0F
P_2_305 = *+1
 lda #$00
 sta $1B
P_2_306 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_307 = *+1
 lda #$00
 sta $0D
P_2_308 = *+1
 lda #$00
 sta $0E
P_2_309 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_310 = *+1
 lda #$00
 sta $09
P_2_311 = *+1
 lda #$00
 sta $08
P_2_312 = *+1
 lda #$00
 sta $0D
P_2_313 = *+1
 lda #$00
 sta $0E
P_2_314 = *+1
 lda #$00
 sta $0F
P_2_315 = *+1
 lda #$00
 sta $1B
P_2_316 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_317 = *+1
 lda #$00
 sta $0D
P_2_318 = *+1
 lda #$00
 sta $0E
P_2_319 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_320 = *+1
 lda #$00
 sta $09
P_2_321 = *+1
 lda #$00
 sta $08
P_2_322 = *+1
 lda #$00
 sta $0D
P_2_323 = *+1
 lda #$00
 sta $0E
P_2_324 = *+1
 lda #$00
 sta $0F
P_2_325 = *+1
 lda #$00
 sta $1B
P_2_326 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_327 = *+1
 lda #$00
 sta $0D
P_2_328 = *+1
 lda #$00
 sta $0E
P_2_329 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_330 = *+1
 lda #$00
 sta $09
P_2_331 = *+1
 lda #$00
 sta $08
P_2_332 = *+1
 lda #$00
 sta $0D
P_2_333 = *+1
 lda #$00
 sta $0E
P_2_334 = *+1
 lda #$00
 sta $0F
P_2_335 = *+1
 lda #$00
 sta $1B
P_2_336 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_337 = *+1
 lda #$00
 sta $0D
P_2_338 = *+1
 lda #$00
 sta $0E
P_2_339 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_340 = *+1
 lda #$00
 sta $09
P_2_341 = *+1
 lda #$00
 sta $08
P_2_342 = *+1
 lda #$00
 sta $0D
P_2_343 = *+1
 lda #$00
 sta $0E
P_2_344 = *+1
 lda #$00
 sta $0F
P_2_345 = *+1
 lda #$00
 sta $1B
P_2_346 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_347 = *+1
 lda #$00
 sta $0D
P_2_348 = *+1
 lda #$00
 sta $0E
P_2_349 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_350 = *+1
 lda #$00
 sta $09
P_2_351 = *+1
 lda #$00
 sta $08
P_2_352 = *+1
 lda #$00
 sta $0D
P_2_353 = *+1
 lda #$00
 sta $0E
P_2_354 = *+1
 lda #$00
 sta $0F
P_2_355 = *+1
 lda #$00
 sta $1B
P_2_356 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_357 = *+1
 lda #$00
 sta $0D
P_2_358 = *+1
 lda #$00
 sta $0E
P_2_359 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_360 = *+1
 lda #$00
 sta $09
P_2_361 = *+1
 lda #$00
 sta $08
P_2_362 = *+1
 lda #$00
 sta $0D
P_2_363 = *+1
 lda #$00
 sta $0E
P_2_364 = *+1
 lda #$00
 sta $0F
P_2_365 = *+1
 lda #$00
 sta $1B
P_2_366 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_367 = *+1
 lda #$00
 sta $0D
P_2_368 = *+1
 lda #$00
 sta $0E
P_2_369 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_370 = *+1
 lda #$00
 sta $09
P_2_371 = *+1
 lda #$00
 sta $08
P_2_372 = *+1
 lda #$00
 sta $0D
P_2_373 = *+1
 lda #$00
 sta $0E
P_2_374 = *+1
 lda #$00
 sta $0F
P_2_375 = *+1
 lda #$00
 sta $1B
P_2_376 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_377 = *+1
 lda #$00
 sta $0D
P_2_378 = *+1
 lda #$00
 sta $0E
P_2_379 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_380 = *+1
 lda #$00
 sta $09
P_2_381 = *+1
 lda #$00
 sta $08
P_2_382 = *+1
 lda #$00
 sta $0D
P_2_383 = *+1
 lda #$00
 sta $0E
P_2_384 = *+1
 lda #$00
 sta $0F
P_2_385 = *+1
 lda #$00
 sta $1B
P_2_386 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_387 = *+1
 lda #$00
 sta $0D
P_2_388 = *+1
 lda #$00
 sta $0E
P_2_389 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_390 = *+1
 lda #$00
 sta $09
P_2_391 = *+1
 lda #$00
 sta $08
P_2_392 = *+1
 lda #$00
 sta $0D
P_2_393 = *+1
 lda #$00
 sta $0E
P_2_394 = *+1
 lda #$00
 sta $0F
P_2_395 = *+1
 lda #$00
 sta $1B
P_2_396 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_397 = *+1
 lda #$00
 sta $0D
P_2_398 = *+1
 lda #$00
 sta $0E
P_2_399 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_400 = *+1
 lda #$00
 sta $09
P_2_401 = *+1
 lda #$00
 sta $08
P_2_402 = *+1
 lda #$00
 sta $0D
P_2_403 = *+1
 lda #$00
 sta $0E
P_2_404 = *+1
 lda #$00
 sta $0F
P_2_405 = *+1
 lda #$00
 sta $1B
P_2_406 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_407 = *+1
 lda #$00
 sta $0D
P_2_408 = *+1
 lda #$00
 sta $0E
P_2_409 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_410 = *+1
 lda #$00
 sta $09
P_2_411 = *+1
 lda #$00
 sta $08
P_2_412 = *+1
 lda #$00
 sta $0D
P_2_413 = *+1
 lda #$00
 sta $0E
P_2_414 = *+1
 lda #$00
 sta $0F
P_2_415 = *+1
 lda #$00
 sta $1B
P_2_416 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_417 = *+1
 lda #$00
 sta $0D
P_2_418 = *+1
 lda #$00
 sta $0E
P_2_419 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_420 = *+1
 lda #$00
 sta $09
P_2_421 = *+1
 lda #$00
 sta $08
P_2_422 = *+1
 lda #$00
 sta $0D
P_2_423 = *+1
 lda #$00
 sta $0E
P_2_424 = *+1
 lda #$00
 sta $0F
P_2_425 = *+1
 lda #$00
 sta $1B
P_2_426 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_427 = *+1
 lda #$00
 sta $0D
P_2_428 = *+1
 lda #$00
 sta $0E
P_2_429 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_430 = *+1
 lda #$00
 sta $09
P_2_431 = *+1
 lda #$00
 sta $08
P_2_432 = *+1
 lda #$00
 sta $0D
P_2_433 = *+1
 lda #$00
 sta $0E
P_2_434 = *+1
 lda #$00
 sta $0F
P_2_435 = *+1
 lda #$00
 sta $1B
P_2_436 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_437 = *+1
 lda #$00
 sta $0D
P_2_438 = *+1
 lda #$00
 sta $0E
P_2_439 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_440 = *+1
 lda #$00
 sta $09
P_2_441 = *+1
 lda #$00
 sta $08
P_2_442 = *+1
 lda #$00
 sta $0D
P_2_443 = *+1
 lda #$00
 sta $0E
P_2_444 = *+1
 lda #$00
 sta $0F
P_2_445 = *+1
 lda #$00
 sta $1B
P_2_446 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_447 = *+1
 lda #$00
 sta $0D
P_2_448 = *+1
 lda #$00
 sta $0E
P_2_449 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_450 = *+1
 lda #$00
 sta $09
P_2_451 = *+1
 lda #$00
 sta $08
P_2_452 = *+1
 lda #$00
 sta $0D
P_2_453 = *+1
 lda #$00
 sta $0E
P_2_454 = *+1
 lda #$00
 sta $0F
P_2_455 = *+1
 lda #$00
 sta $1B
P_2_456 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_457 = *+1
 lda #$00
 sta $0D
P_2_458 = *+1
 lda #$00
 sta $0E
P_2_459 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_460 = *+1
 lda #$00
 sta $09
P_2_461 = *+1
 lda #$00
 sta $08
P_2_462 = *+1
 lda #$00
 sta $0D
P_2_463 = *+1
 lda #$00
 sta $0E
P_2_464 = *+1
 lda #$00
 sta $0F
P_2_465 = *+1
 lda #$00
 sta $1B
P_2_466 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_467 = *+1
 lda #$00
 sta $0D
P_2_468 = *+1
 lda #$00
 sta $0E
P_2_469 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_470 = *+1
 lda #$00
 sta $09
P_2_471 = *+1
 lda #$00
 sta $08
P_2_472 = *+1
 lda #$00
 sta $0D
P_2_473 = *+1
 lda #$00
 sta $0E
P_2_474 = *+1
 lda #$00
 sta $0F
P_2_475 = *+1
 lda #$00
 sta $1B
P_2_476 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_477 = *+1
 lda #$00
 sta $0D
P_2_478 = *+1
 lda #$00
 sta $0E
P_2_479 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_480 = *+1
 lda #$00
 sta $09
P_2_481 = *+1
 lda #$00
 sta $08
P_2_482 = *+1
 lda #$00
 sta $0D
P_2_483 = *+1
 lda #$00
 sta $0E
P_2_484 = *+1
 lda #$00
 sta $0F
P_2_485 = *+1
 lda #$00
 sta $1B
P_2_486 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_487 = *+1
 lda #$00
 sta $0D
P_2_488 = *+1
 lda #$00
 sta $0E
P_2_489 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_490 = *+1
 lda #$00
 sta $09
P_2_491 = *+1
 lda #$00
 sta $08
P_2_492 = *+1
 lda #$00
 sta $0D
P_2_493 = *+1
 lda #$00
 sta $0E
P_2_494 = *+1
 lda #$00
 sta $0F
P_2_495 = *+1
 lda #$00
 sta $1B
P_2_496 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_497 = *+1
 lda #$00
 sta $0D
P_2_498 = *+1
 lda #$00
 sta $0E
P_2_499 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_500 = *+1
 lda #$00
 sta $09
P_2_501 = *+1
 lda #$00
 sta $08
P_2_502 = *+1
 lda #$00
 sta $0D
P_2_503 = *+1
 lda #$00
 sta $0E
P_2_504 = *+1
 lda #$00
 sta $0F
P_2_505 = *+1
 lda #$00
 sta $1B
P_2_506 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_507 = *+1
 lda #$00
 sta $0D
P_2_508 = *+1
 lda #$00
 sta $0E
P_2_509 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_510 = *+1
 lda #$00
 sta $09
P_2_511 = *+1
 lda #$00
 sta $08
P_2_512 = *+1
 lda #$00
 sta $0D
P_2_513 = *+1
 lda #$00
 sta $0E
P_2_514 = *+1
 lda #$00
 sta $0F
P_2_515 = *+1
 lda #$00
 sta $1B
P_2_516 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_517 = *+1
 lda #$00
 sta $0D
P_2_518 = *+1
 lda #$00
 sta $0E
P_2_519 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_520 = *+1
 lda #$00
 sta $09
P_2_521 = *+1
 lda #$00
 sta $08
P_2_522 = *+1
 lda #$00
 sta $0D
P_2_523 = *+1
 lda #$00
 sta $0E
P_2_524 = *+1
 lda #$00
 sta $0F
P_2_525 = *+1
 lda #$00
 sta $1B
P_2_526 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_527 = *+1
 lda #$00
 sta $0D
P_2_528 = *+1
 lda #$00
 sta $0E
P_2_529 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_530 = *+1
 lda #$00
 sta $09
P_2_531 = *+1
 lda #$00
 sta $08
P_2_532 = *+1
 lda #$00
 sta $0D
P_2_533 = *+1
 lda #$00
 sta $0E
P_2_534 = *+1
 lda #$00
 sta $0F
P_2_535 = *+1
 lda #$00
 sta $1B
P_2_536 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_537 = *+1
 lda #$00
 sta $0D
P_2_538 = *+1
 lda #$00
 sta $0E
P_2_539 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_540 = *+1
 lda #$00
 sta $09
P_2_541 = *+1
 lda #$00
 sta $08
P_2_542 = *+1
 lda #$00
 sta $0D
P_2_543 = *+1
 lda #$00
 sta $0E
P_2_544 = *+1
 lda #$00
 sta $0F
P_2_545 = *+1
 lda #$00
 sta $1B
P_2_546 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_547 = *+1
 lda #$00
 sta $0D
P_2_548 = *+1
 lda #$00
 sta $0E
P_2_549 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_550 = *+1
 lda #$00
 sta $09
P_2_551 = *+1
 lda #$00
 sta $08
P_2_552 = *+1
 lda #$00
 sta $0D
P_2_553 = *+1
 lda #$00
 sta $0E
P_2_554 = *+1
 lda #$00
 sta $0F
P_2_555 = *+1
 lda #$00
 sta $1B
P_2_556 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_557 = *+1
 lda #$00
 sta $0D
P_2_558 = *+1
 lda #$00
 sta $0E
P_2_559 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_560 = *+1
 lda #$00
 sta $09
P_2_561 = *+1
 lda #$00
 sta $08
P_2_562 = *+1
 lda #$00
 sta $0D
P_2_563 = *+1
 lda #$00
 sta $0E
P_2_564 = *+1
 lda #$00
 sta $0F
P_2_565 = *+1
 lda #$00
 sta $1B
P_2_566 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_567 = *+1
 lda #$00
 sta $0D
P_2_568 = *+1
 lda #$00
 sta $0E
P_2_569 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_570 = *+1
 lda #$00
 sta $09
P_2_571 = *+1
 lda #$00
 sta $08
P_2_572 = *+1
 lda #$00
 sta $0D
P_2_573 = *+1
 lda #$00
 sta $0E
P_2_574 = *+1
 lda #$00
 sta $0F
P_2_575 = *+1
 lda #$00
 sta $1B
P_2_576 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_577 = *+1
 lda #$00
 sta $0D
P_2_578 = *+1
 lda #$00
 sta $0E
P_2_579 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_580 = *+1
 lda #$00
 sta $09
P_2_581 = *+1
 lda #$00
 sta $08
P_2_582 = *+1
 lda #$00
 sta $0D
P_2_583 = *+1
 lda #$00
 sta $0E
P_2_584 = *+1
 lda #$00
 sta $0F
P_2_585 = *+1
 lda #$00
 sta $1B
P_2_586 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_587 = *+1
 lda #$00
 sta $0D
P_2_588 = *+1
 lda #$00
 sta $0E
P_2_589 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_590 = *+1
 lda #$00
 sta $09
P_2_591 = *+1
 lda #$00
 sta $08
P_2_592 = *+1
 lda #$00
 sta $0D
P_2_593 = *+1
 lda #$00
 sta $0E
P_2_594 = *+1
 lda #$00
 sta $0F
P_2_595 = *+1
 lda #$00
 sta $1B
P_2_596 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_597 = *+1
 lda #$00
 sta $0D
P_2_598 = *+1
 lda #$00
 sta $0E
P_2_599 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_600 = *+1
 lda #$00
 sta $09
P_2_601 = *+1
 lda #$00
 sta $08
P_2_602 = *+1
 lda #$00
 sta $0D
P_2_603 = *+1
 lda #$00
 sta $0E
P_2_604 = *+1
 lda #$00
 sta $0F
P_2_605 = *+1
 lda #$00
 sta $1B
P_2_606 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_607 = *+1
 lda #$00
 sta $0D
P_2_608 = *+1
 lda #$00
 sta $0E
P_2_609 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_610 = *+1
 lda #$00
 sta $09
P_2_611 = *+1
 lda #$00
 sta $08
P_2_612 = *+1
 lda #$00
 sta $0D
P_2_613 = *+1
 lda #$00
 sta $0E
P_2_614 = *+1
 lda #$00
 sta $0F
P_2_615 = *+1
 lda #$00
 sta $1B
P_2_616 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_617 = *+1
 lda #$00
 sta $0D
P_2_618 = *+1
 lda #$00
 sta $0E
P_2_619 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_620 = *+1
 lda #$00
 sta $09
P_2_621 = *+1
 lda #$00
 sta $08
P_2_622 = *+1
 lda #$00
 sta $0D
P_2_623 = *+1
 lda #$00
 sta $0E
P_2_624 = *+1
 lda #$00
 sta $0F
P_2_625 = *+1
 lda #$00
 sta $1B
P_2_626 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_627 = *+1
 lda #$00
 sta $0D
P_2_628 = *+1
 lda #$00
 sta $0E
P_2_629 = *+1
 lda #$00
 sta $0F
 sta $02
P_2_630 = *+1
 lda #$00
 sta $09
P_2_631 = *+1
 lda #$00
 sta $08
P_2_632 = *+1
 lda #$00
 sta $0D
P_2_633 = *+1
 lda #$00
 sta $0E
P_2_634 = *+1
 lda #$00
 sta $0F
P_2_635 = *+1
 lda #$00
 sta $1B
P_2_636 = *+1
 lda #$00
 sta $1C
 bit $80
 nop
P_2_637 = *+1
 lda #$00
 sta $0D
P_2_638 = *+1
 lda #$00
 sta $0E
P_2_639 = *+1
 lda #$00
 sta $0F
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
 lda #0
 sta $04
 sta $05
P_7_0 = *+1
 lda #$38
 ldx #0
 jsr Position
P_7_1 = *+1
 lda #$68
 ldx #1
 jsr Position
 sta $02
 sta $2A
P_7_2 = *+1
 lda #$00
 sta $06
P_7_3 = *+1
 lda #$00
 sta $07
Frame
 lda #2
 sta $01
 sta $00
 sta $02
 sta $02
 sta $02
 lda #0
 sta $00
 ldx #37
Blank
 sta $02
 dex
 bne Blank
 lda #0
 sta $01
 jmp $FF24
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
