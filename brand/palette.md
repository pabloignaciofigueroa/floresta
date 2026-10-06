# Paleta — Floresta (Fase 04)

Método: k-means (k=7, scikit-learn) sobre píxeles muestreados de cada grupo. Script reproducible en `tools/palette.py`.

| Grupo | Archivos | Resultado (por peso) |
|---|---|---|
| Piezas verdes | "Debes saber…", "También puedes venir directamente" | **#406345** 80% · #5e7960 8% · #7c937d 6% · #875d34 · #861c21 · #c98d6d · #da9b11 |
| Piezas salvia | Catálogo: Girasoles, Rosas Rojas, Rosas y Girasoles, Silvestres | **#a8baa2** 82% · #83987f 6% · #461f1a · #775939 · #8f1131 · #b58175 · #ce7b0c |
| Piezas crema | 21 de septiembre, Día de la Novia | **#f7f4ed** 68% · #dacebf 10% · #be9192 · #572f27 · #edc646 · #857b61 · #b52f6a |
| Isotipo | `isotipo.png` (píxeles opacos y semitransparentes) | Pétalos **#f8b0a0** · línea **#305038** · hojas #e4f4e7 al 44% |
| Logotipo | `logotipo.png` | **#32583c** 64% · #284a31 36% |
| Fotos 2025–26 | 79 fotos (una de cada tres) | #2c241c 22% · #4c5747 20% · #b1aba1 17% · #7d7a74 16% · #8b382f 10% · #dfd9d6 8% · #c37b3e 7% |

Lectura: la marca es **verde sobre verde**. Dos campos planos (bosque y salvia) que se alternan, con el grabado botánico en un tono apenas distinto del fondo, más el crema de los anuncios. El color lo ponen las flores (coral del isotipo, amarillo girasol, rojo rosa) y el papel kraft de los envoltorios. Las fotos aportan la madera oscura y el gris cálido del local.

## Tokens (nombre propio de la marca)
| Token | Hex | Origen | Rol |
|---|---|---|---|
| `--bosque` | #406345 | campo de "Debes saber…" | Fondo principal oscuro |
| `--tinta` | #32583c | logotipo | Texto sobre crema, logotipo |
| `--hondo` | #24402b | sombra del logotipo (#284a31), un paso más oscuro | Texto sobre salvia |
| `--salvia` | #a3bba9 | campo del catálogo (píxel plano medido; el centro k-means #a8baa2 incluye el grabado) | Fondo claro de producto; títulos script sobre bosque |
| `--grabado` | #83987f | líneas botánicas sobre salvia | Ilustración de fondo, bordes |
| `--liquen` | #c9d6c4 | entre salvia y crema | Rótulos sobre bosque |
| `--crema` | #f7f4ed | anuncios 21 sept / Novia | Fondo claro editorial; texto sobre bosque |
| `--coral` | #f8b0a0 | pétalos del isotipo | El único acento de interfaz (botón, punto activo, carrito) |
| `--girasol` | #da9b11 | girasoles de las piezas | Solo dentro de ilustración |
| `--kraft` | #875d34 | papel de los envoltorios | Detalles mínimos |
| `--madera` | #2c241c | fotos del local | Fondo de video, velos |

## Contraste (WCAG 2.1, calculado)
| Texto | Fondo | Razón | Uso permitido |
|---|---|---|---|
| crema #f7f4ed | bosque #406345 | 6,19 | Texto corrido ✔ |
| liquen #c9d6c4 | bosque | 4,50 | Rótulos y texto ✔ (AA justo) |
| salvia #a8baa2 | bosque | 3,31 | Solo títulos script ≥ 32 px ✔ |
| coral #f8b0a0 | bosque | 3,79 | Solo elementos grandes / íconos ✔ |
| hondo #24402b | salvia #a3bba9 | 5,55 | Texto corrido ✔ |
| tinta #32583c | salvia | 3,94 | Solo títulos grandes ✔ |
| tinta #32583c | crema | 7,36 | Texto corrido ✔ |
| crema | madera #2c241c | 13,89 | Texto sobre video ✔ |
| grabado #83987f | bosque | 2,19 | Decoración, nunca texto ✘ |

Botón principal: fondo `--coral`, texto `--hondo` (contraste 6,35 calculado).
