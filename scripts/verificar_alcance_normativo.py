#!/usr/bin/env python3
"""MiniHouse · guard de alcance normativo.

Comprueba que las correcciones de alcance ya verificadas no se pierdan
en ediciones futuras:

  1. TEK17 §13-2 no gobierna la ruta mikrohus; rige §13-1(1) con cantidades
     de aire documentadas (S023).
  2. El marco §14-2 no es objetivo de MiniHouse en las rutas probables
     (S020/S021).
  3. En el capítulo 11 rige R 15 (§11-4(3) no. 4), no el R 30 de la Tabla 1,
     y sólo V-01 cumple como ventana de escape (S024).
  4. El capítulo 7 fija F2 = 1/200 y S2 = 1/1000, y las clases no dependen de
     C-01; nieve, viento y sismo son §10-2, no capítulo 7 (S026).
  5. El capítulo 9 no es ruido ni agua, y su §9-2 **no tiene ruta documental sin
     fabricante**; el capítulo 15 **no exime a los edificios pequeños**; el
     capítulo 16 es control de ascensores, no documentación; y §17-1 no alcanza
     a un småhus (S027/S028).
  6. §2-2(2) sólo permite análisis donde la norma da función y **no** número, y
     §2-2(3) exige márgenes declarados; §4-1(2) se rechaza para esta casita
     (S029).

No valida la verdad de las fuentes: eso ya está hecho en
S012/S020/S021/S023/S024/S026/S027/S028/S029.
Sólo detecta regresiones documentales. Sale 0 si todo pasa, 1 si algo falla.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    problems = []

    def require(rel, *needles):
        text = read(rel)
        if text is None:
            problems.append(f"falta archivo: {rel}")
            return
        for needle in needles:
            if needle not in text:
                problems.append(f"{rel}: falta texto obligatorio {needle!r}")

    def forbid(rel, *needles):
        text = read(rel)
        if text is None:
            return
        for needle in needles:
            if needle in text:
                problems.append(f"{rel}: queda texto obsoleto {needle!r}")

    def require_line_context(rel, trigger, allowed):
        text = read(rel)
        if text is None:
            return
        for number, line in enumerate(text.splitlines(), 1):
            if trigger in line and not any(token in line.lower() for token in allowed):
                problems.append(
                    f"{rel}:{number}: {trigger!r} sin acotar; se esperaba uno de {allowed}"
                )

    # Marcadores de las fuentes corregidas.
    require(
        "knowledge/sources/S023.md",
        "§13-2, §13-3, §13-6 and §13-8 do not apply",
        "§13-1(1)",
    )
    require(
        "knowledge/sources/S012.md",
        "SCOPE CORRECTION",
        "not a MiniHouse target",
        "retrieved and scoped in **S023**",
    )
    require(
        "knowledge/sources/S021.md",
        "§14-5",
        "§14-4",
    )

    # Marcadores en síntesis y planificación.
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "NOT applicable to mikrohus route",
        "applicable set is §13-1(1)",
        "NOT APPLICABLE to likely MiniHouse routes",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "NOT applicable to the mikrohus route",
        "§13-1(1) (S023)",
        "not a MiniHouse compliance target",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "§§13-2/3/6/8 exempt",
        "NOT applicable to mikrohus route",
    )
    require("knowledge/INDEX.md", "| S023 |", "| C004 |")
    require(
        "docs/plan-diseno-construccion.md",
        "§13-2 no aplica",
        "S023",
    )
    require("fase1/registro-decisiones.md", "## H.", "S023")
    require("docs/estado-del-plan.md", "30 fuentes", "S023 corrige")
    require(
        "knowledge/competence-memos.md",
        "NOT applicable to the mikrohus route",
        "Chapter 13 route map (S023)",
    )
    require("fase1/solicitud-datos.md", "cantidades de aire alternativas")
    require(
        "fase1/clasificacion-uso-decision.md",
        "Corrección importante sobre ventilación",
    )
    require("docs/auditoria-002.md", "Nota posterior")

    # Marcadores del capítulo 11 (incendio), S024.
    require(
        "knowledge/sources/S024.md",
        "§11-4(3) no. 4",
        "R 15",
        "§11-13(4)",
        "risk class 4",
        "§11-9",
        "§11-10",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "§11-4(3) no. 4 governs: R 15",
        "current apertures FAIL two of three readings",
        "§11-9 D no. 7",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "§11-4(3) no. 4",
        "only **V-01**",
        "D-s2,d0",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "R 15**, not the R 30",
    )
    require("knowledge/INDEX.md", "| S024 |")
    require("docs/plan-diseno-construccion.md", "S024", "V-01")
    require("fase1/registro-decisiones.md", "## I.", "§11-4(3) nº 4")
    require("docs/estado-del-plan.md", "R 15", "sólo V-01")
    require("fase1/verificacion-incendio.md", "Qualifying escape windows: 1")

    # Marcadores del capítulo 12 (S025): conjunto admitido y altura libre.
    require(
        "knowledge/sources/S025.md",
        "§12-7(2)(c)",
        "2.2 m",
        "**exempt**",
        "20.1°",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "NOT applicable to mikrohus route",
        "§12-7(2)(c) room height",
        "Chapter 7 natural hazards",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "only eight provisions apply",
        "§12-7(2)(a)'s **2.4 m is exempt**",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "all accessibility rules and the 2.4 m room height are exempt",
    )
    require("knowledge/INDEX.md", "| S025 |")
    require("docs/plan-diseno-construccion.md", "S025", "riesgos naturales del capítulo 7")
    require("fase1/registro-decisiones.md", "## J.", "§12-7(2)(c)")
    require("docs/estado-del-plan.md", "Altura libre §12-7")
    require("fase1/verificacion-altura-libre.md", "## 3. Largest pitch")

    # Marcadores del capítulo 7 (riesgos naturales), S026.
    require(
        "knowledge/sources/S026.md",
        "F2",
        "1/200",
        "S2",
        "1/1000",
        "marine limit",
        "§10-2",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "§7-2 flood and storm surge",
        "MiniHouse is F2",
        "MiniHouse is S2",
        "marine limit",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "F2 = 1/200",
        "S2 = 1/1000",
        "below the marine limit",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "flood class **F2 (1/200)**",
        "even outside mapped zones",
    )
    require("knowledge/INDEX.md", "| S026 |")
    require("docs/plan-diseno-construccion.md", "S026", "F2 = 1/200", "F3 = 1/1000")
    require("fase1/registro-decisiones.md", "## K.", "F2 = 1/200", "límite marino")
    require("docs/estado-del-plan.md", "F2 = 1/200", "S026")
    require(
        "fase1/cribado-riesgos-naturales.md",
        "NO SITE, NO HAZARD MAP, NO GEOTECHNICAL ASSESSMENT",
        "quick clay",
        "no pass state",
    )

    # Marcadores de la envolvente (§14-3 / §13-13).
    require(
        "knowledge/comparisons/module-brief.md",
        "0.267",
        "189 mm",
        "cold-side trap",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "§14-3 element screening",
        "all three fail",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "all three exceed §14-3",
        "0.41 kg/m²",
    )
    require("knowledge/INDEX.md", "| envelope-check.json |")
    require("docs/plan-diseno-construccion.md", "verificacion-envolvente", "189 mm")
    require("fase1/registro-decisiones.md", "## L.", "189 mm", "trampa en el lado frío")
    require("docs/estado-del-plan.md", "Envolvente §14-3")
    require(
        "fase1/verificacion-envolvente.md",
        "NO PRODUCTS SELECTED",
        "Glaser",
        "not counted",
    )

    # Marcadores de la sección integrada (altura + pendiente + envolvente + gálibo).
    require(
        "fase1/verificacion-seccion.md",
        "PARAMETRIC, NO GEOMETRY FROZEN",
        "t/cos θ",
        "not achievable",
        "1785",
    )
    require("knowledge/comparisons/module-brief.md", "1785", "16.3°", "closed")
    require("knowledge/comparisons/compliance-matrix.md", "Integrated height, pitch and transport")
    require("knowledge/comparisons/known-assumed-unknown.md", "1785", "4.5 m²")
    require("knowledge/INDEX.md", "| section-feasibility.json |")
    require("docs/plan-diseno-construccion.md", "verificacion-seccion", "1785")
    require("fase1/registro-decisiones.md", "## M.", "1785", "t/cos θ")
    require("docs/estado-del-plan.md", "Sección integrada")
    # La comprobación anterior de altura libre debe seguir declarando su alcance.
    require("fase1/verificacion-altura-libre.md", "Superseded in scope, not in arithmetic")

    # Marcadores de las opciones R2 y su tolerancia.
    require(
        "fase1/opciones-seccion-R2.md",
        "OPTIONS — NO SELECTION",
        "not a robust option",
        "gives a loft",
    )
    require("knowledge/comparisons/module-brief.md", "R2-B", "1141 mm", "100 mm")
    require("knowledge/comparisons/compliance-matrix.md", "No option has tolerance")
    require("knowledge/comparisons/known-assumed-unknown.md", "6.24 m² in plan")
    require("knowledge/INDEX.md", "| section-options.json |")
    require("docs/plan-diseno-construccion.md", "opciones-seccion-R2")
    require("fase1/registro-decisiones.md", "## N.", "R2-B")
    require("docs/estado-del-plan.md", "Opciones R2")

    # Marcadores de los capítulos 9, 15, 16 y 17 (S027, S028).
    # El punto que no puede perderse es que §9-2 NO tiene ruta documental sin
    # fabricante: si esa frase desaparece, la madera recuperada parece resuelta.
    require(
        "knowledge/sources/S027.md",
        "Reclaimed timber has no manufacturer",
        "§9-6",
        "10 tonnes",
        "second siting gate",
        "existing buildings only",
    )
    require(
        "knowledge/sources/S028.md",
        "no exemption for small buildings",
        "0.90 m",
        "two free sides",
        "T400",
        "Sikkerhetskontroll av heis",
    )
    require(
        "fase1/verificacion-instalaciones.md",
        "NO PRODUCT SELECTED",
        "cannot be crossed by building the cabin",
        "minimum burial depth",
        "operational-safety regime, not documentation",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "no documented route for reclaimed timber",
        "second siting gate",
        "engages only through the 10-tonne limb",
        "NOT applicable — and not a documentation chapter",
        "NOT applicable by definition",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "no documented route",
        "no small-building exemption anywhere",
        "minimum burial depth",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "no manufacturer-free compliance route",
        "cannot be crossed by building an 18 m² cabin",
        "Chapter 16 is lift safety control, not documentation",
    )
    require("knowledge/INDEX.md", "| S027 |", "| S028 |", "| instalaciones-check.json |")
    require("docs/plan-diseno-construccion.md", "S027", "S028", "dos puertas de emplazamiento")
    require("fase1/registro-decisiones.md", "## O.", "## P.", "suponen un fabricante")
    require("docs/estado-del-plan.md", "Capítulo 9 medio exterior", "Capítulos 15/16/17")
    require("fase1/solicitud-datos.md", "derribo del origen", "ensayos de la madera")

    # La pantalla de izaje debe seguir separando geometría de masa: el ranking es
    # invariante con la masa y las masas de ejemplo no son datos de proyecto.
    require(
        "knowledge/comparisons/lift-geometry-screen.md",
        "ranking of layouts and verticals is mass-independent",
        "None of them is project data",
    )

    # Marcadores de los capítulos 2 y 4 (S029).
    require(
        "knowledge/sources/S029.md",
        "allowed only where no number was given",
        "necessary safety margins",
        "considered and rejected",
        "not retrieved",
        "ajour",
    )
    require(
        "fase1/verificacion-documentacion.md",
        "AUDIT — NOT A COMPLIANCE STATEMENT",
        "cannot analyse your way past a stated performance",
        "none stated",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "§2-2(1)+(2) the gate",
        "CONSIDERED AND REJECTED",
        "fully carded",
    )
    require("knowledge/comparisons/module-brief.md", "judges the method", "§2-2(3)")
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "only where the regulation gives a function and no number",
        "6 of 6 FDV categories",
    )
    require("knowledge/INDEX.md", "| S029 |", "| documentacion-check.json |")
    require("docs/plan-diseno-construccion.md", "S029", "un solo margen coherente")
    require("fase1/registro-decisiones.md", "## Q.", "Considerada y rechazada")
    require("docs/estado-del-plan.md", "Capítulos 2/4 documentación")

    # Puentes térmicos: §14-3 no los limita, el 0,05 es de §14-2 (exento), y la
    # referencia normalizada no es adoptable a 18 m². Es una corrección propia:
    # la primera versión del informe decía que no se podían compensar.
    require(
        "fase1/verificacion-puentes-termicas.md",
        "§14-3 sets no thermal-bridge limit",
        "geometrically closed",
        "wrong, and the self-test in this script is what caught it",
        "do not adopt 0.05 W/m²K as a MiniHouse target",
        "61.10",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "VERIFIED absence of a limit",
        "unbounded by the regulation",
        "state targets **per metre**",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "no requirement is watching",
        "per metre",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "§14-3 sets no thermal-bridge limit",
        "mis-specified at 18 m²",
    )
    require("knowledge/INDEX.md", "| puentes-termicas.json |", "| ../scripts/puentes_termicas.py |")
    require("docs/plan-diseno-construccion.md", "encuentro chasis-pared", "el mismo dibujo")
    require("docs/estado-del-plan.md", "Puentes térmicos del chasis")
    require("fase1/registro-decisiones.md", "## R.", "Era falso; lo detectó el autotest")

    # La declaración de márgenes de §2-2(3): una moneda por tipo, signos explícitos,
    # «indefinido» como entrada válida y R2 como requisito, no como preferencia.
    require(
        "fase1/declaracion-de-margenes.md",
        "value available − value required",
        "two rows are positive",
        "stated on the **worst** window",
        "No row clears the test",
        "undefined is a legitimate entry",
        "double-counts",
        "regulatory requirement",
        "It is short of margin",
    )
    require("fase1/verificacion-documentacion.md", "short of margin",
        "2 are positive, 6 negative")
    require("knowledge/INDEX.md", "| ../fase1/declaracion-de-margenes.md |")
    require("knowledge/comparisons/compliance-matrix.md", "the project is short of margin")
    require("knowledge/comparisons/module-brief.md", "Margin blocker (§2-2(3))")
    require("knowledge/comparisons/known-assumed-unknown.md", "F2/S2 classes are themselves the margin")
    require("fase1/registro-decisiones.md", "## S.", "R2 deja de ser preferencia")
    require("docs/estado-del-plan.md", "Declaración de márgenes §2-2(3)")
    require("docs/plan-diseno-construccion.md", "Comprar margen donde se pueda")

    # Condensación del encuentro: §14-3 y §13-13 no cubren la temperatura del acero.
    # La fórmula de f_Rsi se puede invertir por error (0,236 vs 0,765): el autotest
    # lo bloquea, y estos needles bloquean que el texto pierda la conclusión.
    require(
        "fase1/verificacion-condensacion-union.md",
        "neither covers it",
        "0.236",
        "5.9",
        "0.358 m²K/W",
        "Mould governs, not condensation",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "moisture problem before it is an energy problem",
        "0.0002 m²K/W",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "moisture problem before it is an energy problem",
        "Size for mould, not for condensation",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "Mould governs over condensation",
        "visible indoors",
    )
    require("knowledge/INDEX.md", "| condensacion-union.json |", "| ../scripts/condensacion_union.py |")
    require("docs/plan-diseno-construccion.md", "condensación en ese mismo encuentro")
    require("docs/estado-del-plan.md", "Condensación del encuentro")
    require("fase1/registro-decisiones.md", "## T.", "es catastrófico")

    # Cubierta bajo el capítulo 11: las cuatro ramas convergen en A2-s1,d0, así que
    # la duda de interpretación NO bloquea el paquete; R 15 sí, por carbonización.
    require(
        "fase1/determinacion-cubierta-incendio.md",
        "insulation column is identical in all four rows",
        "the roof build-up can be frozen now",
        "no. 6.2 is unavailable",
        "48 mm",
        "78 mm",
        "geometry result",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "does not block the build-up",
        "R 15 is a charring problem",
        "geometry result, not a material property",
    )
    require("knowledge/comparisons/module-brief.md", "can be frozen now", "three clauses, one drawing")
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "does not block the build-up",
        "stud fraction is width ÷ centres",
    )
    require("knowledge/INDEX.md", "| cubierta-incendio.json |", "| ../scripts/cubierta_incendio.py |")
    require("docs/plan-diseno-construccion.md", "Congelar la cubierta", "ancho y separación")
    require("docs/estado-del-plan.md", "Cubierta bajo capítulo 11")
    require("fase1/registro-decisiones.md", "## U.", "duplica su ancho")

    # Ventanas: §11-13 tiene tres lecturas y hay que construir la más estricta.
    # La frase «one accessible escape window is sufficient» es de acceso de bomberos,
    # no una relajación de «vinduer»; y el arreglo de escape es también el de luz diurna.
    require(
        "fase1/verificacion-ventanas.md",
        "**not** a relaxation of «vinduer»",
        "three readings",
        "**R-A** minimal",
        "**R-B** fire cell",
        "**R-C** room by room",
        "no direct exit",
        "two equal minima",
        "escape fix is **also**",
        "150 mm",
        "they do not cancel",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "§11-13 has three readings",
        "about a different requirement",
        "largest dimensional one in the project",
    )
    require("knowledge/comparisons/module-brief.md", "cheapest thing in the project to get right")
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "three readings",
        "**not** a relaxation of «vinduer»",
        "two equal minima",
    )
    require("knowledge/INDEX.md", "| ventanas.json |", "| ../scripts/ventanas_check.py |")
    require("docs/plan-diseno-construccion.md", "cribado de ventanas", "servicio de bomberos")
    require("docs/estado-del-plan.md", "Ventanas §11-13 / §13-7")
    require("fase1/registro-decisiones.md", "## W.", "el único sitio donde una decisión arregla dos cribados")
    require("fase1/declaracion-de-margenes.md", "stated on the **worst** window", "verificacion-ventanas.md")

    # Adecuación de márgenes: §2-2(3) exige márgenes *necesarios*, y la declaración
    # misma define adecuado como positivo Y mayor que su incertidumbre. Ninguna fila pasa.
    require(
        "fase1/verificacion-incertidumbre.md",
        "not adequate",
        "Four kinds of uncertainty",
        "zero by construction",
        "not demonstrated",
        "one-sided",
        "−498 mm",
        "0 adequate",
    )
    require("fase1/declaracion-de-margenes.md", "No row clears the test", "−498 mm")
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "not one row",
    )
    require("knowledge/comparisons/module-brief.md", "not one row clears")
    require("knowledge/comparisons/known-assumed-unknown.md", "No declared margin is adequate")
    require("knowledge/INDEX.md", "| incertidumbre.json |", "| ../scripts/incertidumbre.py |")
    require("docs/plan-diseno-construccion.md", "adecuación de los márgenes")
    require("docs/estado-del-plan.md", "Adecuación de márgenes")
    require("fase1/registro-decisiones.md", "## X.", "Ninguna fila pasa el test")

    # El encuentro resuelto en 2D: el 1D era pesimista con el acero, el punto frío
    # se muda a la esquina de madera al primer milímetro, y envolver el acero gana.
    require(
        "fase1/verificacion-puente-2d.md",
        "SCREENING — CONDITIONAL ON C-01",
        "The solver is validated before it is used",
        "converged to **±0.005** at 2 mm",
        "The 3 mm and 4 mm grids are **not** used",
        "The steel is a parameter, not a profile.",
        "Only **A** and **E** clear it.",
        "The coldest point leaves the steel at the first millimetre of pad.",
        "20 mm reaches 0.754",
        "20 mm, not 9",
        "pessimistic",
        "run the insulation outside the steel.",
        "3.01 W/K",
        "16 %",
        "The generic value sits between them",
        # §9: el rastrel perimetral es una vía paralela, no un puente de unión.
        "an element problem wearing a junction's clothes",
        "must not both count the same joist",
        "referenced to the joisted floor U, the junction reads",
        "0.1716",
        "once every joist spacing, and a point bridge is a 3D effect",
    )
    require(
        "fase1/verificacion-condensacion-union.md",
        "and it has now been measured",
        "direction of the error was backwards",
        "stops governing as soon as it is built",
        "**0.80 m²K/W**",
        "0.44 m²K/W short",
    )
    require(
        "fase1/declaracion-de-margenes.md",
        "0.80** (2D)",
        "−0.80 / −0.39",
        "the sign was inverted by 2D",
        "a **position**, not only a thickness",
        "verificacion-puente-2d.md",
    )
    require(
        "fase1/verificacion-incertidumbre.md",
        "Row 13's sign was inverted, not merely uncertain.",
        "sign inverted by 2D",
        "−0.80",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "The 1D condensation requirement was sized on a surface that stops governing",
        "Padding the steel is the wrong fix",
        "3.01 W/K",
        "A plate is not a chassis member",
        "one junction now calculated",
        "an element problem wearing a junction's clothes",
        "must not both count the same joist",
        "0.1716",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "it changed the answer twice",
        "0.80 m²K/W — 20 mm of rigid foam, not 9",
        "The better fix is not a thickness at all",
        "3.01 W/K",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "In 2D the same plate reads **0.377**",
        "first millimetre of pad",
        "Wrapping the steel **below the floor",
        "0.80 m²K/W — 20 mm of foam, not 9",
    )
    require("knowledge/INDEX.md", "| puente-2d.json |", "| ../scripts/puente_2d.py |",
            "| ../fase1/verificacion-puente-2d.md |",
            "the perimeter joist as parallel-path conduction rather than a junction")
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "parallel-path conduction (U **0.1363 → 0.1716**",
        "unchanged at **+0.028**",
    )
    require(
        "fase1/registro-decisiones.md",
        "no pueden contar el mismo rastrel dos veces",
        "**+0,028**",
    )
    require(
        "docs/plan-diseno-construccion.md",
        "El cálculo 2D ya está hecho y corrige dos cosas",
        "0,80 m²K/W — 20 mm de espuma, no 9",
        "pasar el acero por debajo del suelo",
        "2 positivas, 6 negativas, 3 indefinidas y 2 nulas",
    )
    require("docs/estado-del-plan.md", "**cálculo 2D**", "0,80 m²K/W — 20 mm de espuma, no 9", "3,01 W/K")
    require(
        "fase1/registro-decisiones.md",
        "## Y.",
        "el acero no es el punto frío",
        "3,01 W/K",
        "La fila 13 de la declaración pasa de +0,051 a **−0,39**",
    )


    # Estrategia de incendio: §11-13(4) y §11-14 dependen de la MISMA decisión, y §11-9 no.
    require(
        "fase1/determinacion-estrategia-incendio.md",
        "NOT A FIRE-ENGINEERING ANALYSIS",
        "The allowance is written as an **alternative**",
        "§11-14 then governs the **rømningsvei**",
        "one determination read three ways",
        "P1's cost is nothing, and that is the whole difficulty",
        "**That is wrong, and it is wrong in both directions.**",
        "**5.04 m**",
        "+10.0 m",
        "the applicable row has never been read",
        "it is one question",
    )
    require(
        "fase1/declaracion-de-margenes.md",
        "Three of these rows are one determination",
        "1 positive / 4 negative / 3 undefined /",
        "the answer that keeps reclaimed timber exposed",
        "a large margin and cannot be declared",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "The escape windows and the door width are one determination, not two",
        "What is not coupled is §11-9",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "are one question, and the project had been pricing them as two",
        "What is not coupled is §11-9",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "engaged by the **same** question",
        "48.5 m²",
    )
    require("knowledge/INDEX.md", "| estrategia-incendio.json |",
            "| ../scripts/estrategia_incendio.py |",
            "| ../fase1/determinacion-estrategia-incendio.md |")
    require(
        "docs/plan-diseno-construccion.md",
        "una sola pregunta de incendio",
        "0,29 m²",
    )
    require("docs/estado-del-plan.md", "Estrategia de incendio cap. 11", "1 positiva / 4 negativas")
    require("fase1/registro-decisiones.md", "## Z.", "son una sola pregunta", "48,5 m²")

    # Ventilación §13-1(1): los caudales documentados son lo de menos; lo que
    # aparece es la PRESIÓN, y con ella el primer margen de SEGURIDAD negativo.
    require(
        "fase1/verificacion-ventilacion.md",
        "SCREENING — CONDITIONAL ON C-01",
        "a fan in a sealed box does not move air",
        "**no — the fan stalls**",
        "**−130 Pa**",
        "§13-5 applies to this building",
        "its own outdoor air intake",
        "A steady-state mass balance without the timber buffering gives an indoor "
        "concentration above saturation",
        "the 50 % assumption is conservative",
        "adopted voluntarily",
        "They do not bind on this route and must not be reported as a requirement.",
    )
    require(
        "fase1/declaracion-de-margenes.md",
        "| 14 | Ventilation §13-1(1) — flue",
        "Seven are negative",
        "**Rows 13 and 14 are the same drawing.**",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "A mechanical extract in a sealed cabin does not move air",
        "**rows 13 and 14 are the same drawing**",
    )
    require(
        "knowledge/comparisons/module-brief.md",
        "And the ventilation that keeps that junction dry is what puts the stove at risk",
        "Rows 13 and 14 of the declaration are the same drawing",
    )
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "A sealed 36.9 m³ cabin at 1.5 h⁻¹ @50 Pa holds **106–140 Pa**",
        "The flue reverses by **−130 Pa**",
    )
    require("knowledge/INDEX.md", "| ventilacion.json |",
            "| ../scripts/ventilacion_check.py |",
            "| ../fase1/verificacion-ventilacion.md |")
    require(
        "docs/plan-diseno-construccion.md",
        "**El tiro se invierte: −130 Pa.**",
        "**las filas 13 y 14 son el mismo dibujo**",
    )
    require("docs/estado-del-plan.md", "Ventilación §13-1(1)", "el único margen de **seguridad**")
    require(
        "fase1/registro-decisiones.md",
        "## AA.",
        "las filas 13 y 14 son el mismo dibujo",
        "Margen **−130 Pa**",
    )
    # El margen se calcula SÓLO con presiones alcanzables. Citar los 406 Pa del
    # caso con los dos baños forzados habría dado −396 Pa y exagerado el caso;
    # ese caudal no se entrega, así que no es una presión a la que la casita esté.
    forbid("fase1/verificacion-ventilacion.md", "**−396", "**-396")
    forbid("fase1/declaracion-de-margenes.md", "| −396", "| -396", "**−396", "**-396")

    # El aire de reposición: tiene tamaño, resuelve la ventilación y NO el tiro.
    # La fila 14 no mejora con un agujero; se retira con una estufa estanca.
    require(
        "fase1/verificacion-aporte-aire.md",
        "SCREENING — CONDITIONAL ON C-01",
        "The hole, sized",
        "**113 mm** at **10 Pa** of design",
        "**A passive inlet cannot hold a set pressure**",
        "does not depend on the 125 mm size limit",
        "Row 14 is retired, not improved",
        "**Row 14 therefore does not become positive; it stops being a margin.**",
        "**905**",
        "**0.8 %**",
        "a control problem, not a diffusion problem",
        "a factor of **14.9**",
        "**Not a ventilation design.**",
    )
    require(
        "fase1/declaracion-de-margenes.md",
        "| 14 | Ventilation §13-1(1) — flue",
        "only a room-sealed stove retires it",
        "**Row 14 is the only negative row with a costless resolution, and it has not been "
        "adopted.**",
        "it stops being a margin",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "The make-up air has a size, and it does not buy the flue",
        "**row 14 is retired, not improved**",
    )
    require("knowledge/comparisons/module-brief.md",
            "That hole now has a size, and it does not buy the flue.")
    require(
        "knowledge/comparisons/known-assumed-unknown.md",
        "A **113 mm** inlet at **10 Pa** of design depression",
        "A **room-sealed** stove retires row 14",
    )
    require("knowledge/INDEX.md", "| aporte-aire.json |",
            "| ../scripts/aporte_aire.py |",
            "| ../fase1/verificacion-aporte-aire.md |")
    require(
        "docs/plan-diseno-construccion.md",
        "**113 mm** a **10 Pa** de depresión de diseño",
        "**se retira con una estufa estanca**",
    )
    require("docs/estado-del-plan.md",
            "**El aire de reposición tiene tamaño y no compra el tiro.**")
    require(
        "fase1/registro-decisiones.md",
        "## AB.",
        "**se retira, no se mejora**",
        "**1,65× el cerramiento**",
    )
    require("fase1/verificacion-incertidumbre.md",
            "the only negative row whose resolution is not a number")
    # La pérdida del cerramiento es una sola cifra en todo el proyecto. El informe
    # 2D llevaba 19,4 W/K tecleado a mano; la derivación da 18,3.
    require("fase1/verificacion-puente-2d.md",
            "18.3 W/K at the §14-3 limits",
            "[the make-up air screen](verificacion-aporte-aire.md)")
    forbid("fase1/verificacion-puente-2d.md", "19.4 W/K")

    # El bucle cerrado de R2: los espesores publicados eran redondos, y la dispensa
    # de 4 400 mm no alcanza. Es una corrección propia y tiene que sobrevivir.
    require(
        "fase1/opciones-seccion-R2.md",
        "They do not.",
        "nearly cancel",
        "4400 mm was never the threshold",
        "short by 22 mm",
        "state the member width",
        "only R2-A and R2-C survive it",
    )
    require(
        "knowledge/comparisons/compliance-matrix.md",
        "R2-D's 4400 mm dispensation is 22 mm short",
        "only lever on the section",
    )
    require("knowledge/comparisons/known-assumed-unknown.md", "R2-D's 4400 mm is 22 mm short")
    require("fase1/declaracion-de-margenes.md", "22 mm short", "−422 mm")
    require("fase1/registro-decisiones.md", "## V.", "no basta")
    require("docs/plan-diseno-construccion.md", "los 4 400 mm de R2-D **no bastan**")
    require("docs/estado-del-plan.md", "4 415–4 422")

    # Textos obsoletos que ya fueron corregidos.
    forbid(
        "knowledge/sources/S012.md",
        "Other §13 sections",
        "not yet retrieved",
    )
    forbid(
        "knowledge/comparisons/compliance-matrix.md",
        "Other §13 sections",
        "Remaining TEK17 §13 sections",
        "required to verify the energy frame",
    )
    forbid(
        "knowledge/comparisons/module-brief.md",
        "Other §13 sections",
        "Remaining §13 sections",
    )
    forbid(
        "knowledge/comparisons/known-assumed-unknown.md",
        "Remaining TEK17 §13 sections",
    )
    forbid("knowledge/INDEX.md", "minor §13 sections")
    forbid("knowledge/competence-memos.md", "minor §13 sections")
    forbid("docs/estado-del-plan.md", "19 fuentes")
    forbid("docs/estado-del-plan.md", "21 comprobaciones", "22 comprobaciones", "23 comprobaciones")
    # La afirmación errónea que el autotest desmintió: la compensación sí es posible.
    forbid(
        "fase1/verificacion-puentes-termicas.md",
        "cannot be compensated by insulation",
        "the target goes **negative**",
    )
    forbid("fase1/registro-decisiones.md", "criterio conservador de vivienda")

    # El 1D no puede volver a presentarse como cota conservadora del edificio: el 2D
    # dio 0,377 para el acero (más alto) y mudó el punto frío a la esquina de madera.
    forbid(
        "fase1/verificacion-condensacion-union.md",
        "1D upper bound",
        "No 2D calculation",
    )
    forbid(
        "fase1/declaracion-de-margenes.md",
        "positive on paper",
        "1D value is an upper bound",
    )
    forbid("knowledge/comparisons/compliance-matrix.md", "Every f_Rsi here is a **1D upper bound**")
    forbid("knowledge/comparisons/module-brief.md", "Every value is a 1D upper bound")
    forbid("docs/plan-diseno-construccion.md", "cota superior 1D")
    forbid("docs/estado-del-plan.md", "0,358 m²K/W")

    # El capítulo 7 ya no puede volver a figurar como pendiente de consulta.
    forbid("knowledge/comparisons/compliance-matrix.md", "NOT YET RETRIEVED")
    forbid("knowledge/sources/S025.md", "not yet retrieved")
    forbid("docs/plan-diseno-construccion.md", "Capítulo aún no consultado")
    forbid("docs/estado-del-plan.md", "sigue sin consultarse")

    # El capítulo 16 no puede volver a describirse como capítulo de documentación,
    # ni el 15 como exento para edificios pequeños.
    forbid(
        "knowledge/comparisons/compliance-matrix.md",
        "Chapter 16 documentation",
        "chapter 15 exempt",
        "no small-building rule",
    )
    forbid("knowledge/comparisons/module-brief.md", "chapter 15 exempt", "small buildings are exempt")
    forbid("fase1/registro-decisiones.md", "capítulo 16 de documentación")

    # Cualquier cifra antigua debe aparecer acompañada de su excepción.
    require_line_context(
        "knowledge/comparisons/module-brief.md",
        "21.6 m³/h",
        ("not applicable", "do not carry over", "not a minihouse target"),
    )
    require_line_context(
        "docs/plan-diseno-construccion.md",
        "21,6 m³/h",
        ("no usar", "no aplica", "s023"),
    )
    require_line_context(
        "fase1/registro-decisiones.md",
        "21,6 m³/h",
        ("no trasladar", "impide usar", "s023", "no vincula", "voluntariamente"),
    )
    require_line_context(
        "knowledge/comparisons/module-brief.md",
        "188.9",
        ("not a minihouse compliance target", "not a minihouse target"),
    )
    require_line_context(
        "knowledge/comparisons/compliance-matrix.md",
        "100+1600/A",
        ("arithmetic only", "not applicable"),
    )
    require_line_context(
        "fase1/registro-decisiones.md",
        "188.9",
        ("impide usar", "s021"),
    )

    # R 30 no debe aparecer como requisito sin su excepción §11-4(3) no. 4.
    for rel in (
        "knowledge/comparisons/module-brief.md",
        "knowledge/comparisons/compliance-matrix.md",
        "fase1/registro-decisiones.md",
    ):
        require_line_context(rel, "R 30", ("not the", "table 1", "tabla 1", "superseded"))

    if problems:
        for item in problems:
            print("FALLO:", item)
        print(f"ALCANCE NORMATIVO: {len(problems)} PROBLEMA(S)")
        return 1

    print("ALCANCE NORMATIVO: TODOS LOS MARCADORES Y EXCEPCIONES PASAN")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
