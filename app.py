"""Juego de la placa base ASRock FM2A68M-DG3+ (Streamlit).

Juego 1: 24 componentes de la placa.
Juego 2: 14 elementos del panel trasero.
Modos: "Relacionar todo" y "¿Qué número es?".
"""
import random
from pathlib import Path

import streamlit as st

BASE = Path(__file__).parent

st.set_page_config(page_title="Juego: placa base", page_icon="🧩", layout="wide")


def it(num, name, silk, desc):
    return {"num": num, "name": name, "silk": silk, "desc": desc}


GAMES = {
    "juego1": {
        "title": "Juego 1 · Componentes de la placa",
        "image": "assets/placa_componentes.png",
        "items": [
            it(1, "Zócalo del procesador (Socket FM2+)", "SOCKET FM2b", "Aloja el procesador AMD (FM2+/FM2) y lo conecta con la placa."),
            it(2, "Soporte del disipador", "Sin serigrafía", "Anclaje de plástico donde se fija el disipador de la CPU."),
            it(3, "Ranuras de RAM DIMM DDR3", "DDR3_A1, DDR3_B1", "Alojan los módulos de memoria DDR3 (doble canal, máx. 32 GB)."),
            it(4, "Conector ATX de 24 pines", "ATXPWR1", "Recibe el cable principal de la fuente de alimentación."),
            it(5, "Conector ATX 12 V de 4 pines", "ATX12V1", "Alimenta específicamente al procesador."),
            it(6, "VRM (bobinas y condensadores)", "Sin serigrafía", "Convierte los 12 V de la fuente en la tensión baja y estable del procesador."),
            it(7, "Chipset AMD A68H", "AMD A68H (Bolton-D2H)", "Coordina SATA, USB, PCI, audio y red con el procesador."),
            it(8, "Conectores SATA3", "SATA_1 … SATA_4", "Conectan discos duros, SSD y unidades ópticas (hasta 6 Gb/s)."),
            it(9, "Ranura PCI Express x16", "PCIE1", "Para la tarjeta gráfica dedicada (PCIe 3.0 con CPU FM2+)."),
            it(10, "Ranura PCI Express x1", "PCIE2", "Para tarjetas pequeñas: sonido, USB, SATA, red…"),
            it(11, "Ranura PCI", "PCI1", "Ranura clásica, antigua y más lenta, para tarjetas PCI."),
            it(12, "Pila CMOS (CR2032)", "CMOS BATTERY", "Mantiene la hora y la configuración de la UEFI con el equipo apagado."),
            it(13, "Jumper Clear CMOS", "CLRCMOS1", "Puente de 3 pines que borra la configuración de la UEFI."),
            it(14, "Chip de la BIOS/UEFI", "BIOS (64Mb)", "Guarda el firmware UEFI que arranca la placa."),
            it(15, "Chip Super I/O", "Super I/O", "Gestiona PS/2, puertos heredados y sensores de temperatura/ventiladores."),
            it(16, "Cabecera del puerto paralelo (LPT1)", "LPT1", "Para añadir un puerto paralelo (impresora antigua)."),
            it(17, "Cabecera del puerto serie (COM1)", "COM1", "Para añadir un puerto serie RS-232."),
            it(18, "Cabeceras USB 2.0 internas", "USB_7_8 y USB_9_10", "Conectan los USB frontales de la caja (2 puertos cada una)."),
            it(19, "Cabecera USB flexible", "USB_11_12", "Admite un panel USB 3.0 frontal, pero a velocidad USB 2.0."),
            it(20, "Cabecera del panel frontal (PANEL1)", "PANEL1 / SPEAKER1", "Botón de encendido, reset y LEDs de la caja."),
            it(21, "Chip de red LAN (Realtek)", "LAN", "Controlador Gigabit Ethernet del puerto RJ-45."),
            it(22, "Conector del ventilador de la caja", "CHA_FAN1", "Alimenta y controla un ventilador del chasis."),
            it(23, "Conector del ventilador de la CPU", "CPU_FAN1", "Alimenta y controla el ventilador del disipador."),
            it(24, "Cabecera TPM", "TPMS1", "Para un módulo TPM que guarda claves y certificados."),
        ],
    },
    "juego2": {
        "title": "Juego 2 · Panel trasero",
        "image": "assets/panel_trasero.png",
        "items": [
            it(1, "PS/2 teclado/ratón", "—", "Conector PS/2 combinado para teclado o ratón antiguo."),
            it(2, "USB 2.0 (USB_1_2)", "USB_1_2", "Dos puertos USB 2.0 apilados (480 Mb/s)."),
            it(3, "DVI-D", "DVI1", "Salida de vídeo digital, hasta 2560×1600. No lleva audio."),
            it(4, "VGA (D-Sub)", "VGA1", "Salida de vídeo analógica, hasta 1920×1200."),
            it(5, "USB 3.0 (azules)", "USB_3_4", "Dos puertos USB 3.0 de hasta 5 Gb/s."),
            it(6, "USB 2.0 (USB_5_6)", "USB_5_6", "Dos puertos USB 2.0 junto al RJ-45."),
            it(7, "RJ-45 LAN", "LAN", "Red Gigabit 10/100/1000 con LEDs de enlace y velocidad."),
            it(8, "Line In (azul claro)", "Line In", "Entrada de audio de línea."),
            it(9, "Front Speaker (verde lima)", "Front Speaker", "Salida de audio para altavoces o auriculares."),
            it(10, "Micrófono (rosa)", "Microphone", "Entrada de micrófono."),
            it(11, "Conector ATX 12 V", "ATX12V1", "Alimentación del procesador (referencia en la foto)."),
            it(12, "Zócalo del procesador", "SOCKET FM2b", "Aloja el procesador (referencia en la foto)."),
            it(13, "Ranuras DIMM DDR3", "DDR3_A1, DDR3_B1", "Alojan la memoria RAM (referencia en la foto)."),
            it(14, "Chipset AMD A68H", "AMD A68H", "Controla SATA, USB y demás periféricos (referencia en la foto)."),
        ],
    },
}


# ------------------------------------------------------------------ utilidades
def reset_game(gkey):
    for k in list(st.session_state.keys()):
        if k.endswith(f"_{gkey}") or f"_{gkey}_" in k:
            del st.session_state[k]


def show_image(game):
    path = BASE / game["image"]
    if path.exists():
        try:
            st.image(str(path), width="stretch")  # Streamlit reciente
        except TypeError:
            st.image(str(path), use_container_width=True)  # Streamlit antiguo
    else:
        st.error(f"No se encuentra la imagen: {game['image']}")


# --------------------------------------------------------------- modo relacionar
def mode_match(gkey, game, show_hint):
    items = game["items"]
    names = [i["name"] for i in items]

    order_key = f"order_{gkey}"
    if order_key not in st.session_state:
        shuffled = names[:]
        random.shuffle(shuffled)
        st.session_state[order_key] = shuffled
    options = st.session_state[order_key]

    col_img, col_form = st.columns([3, 2], gap="large")
    with col_img:
        show_image(game)
    with col_form:
        st.markdown("**Elige el nombre que corresponde a cada número:**")
        box = st.container(height=640)
        with box:
            for i in items:
                label = f"Nº {i['num']}"
                if show_hint:
                    label += f"  (serigrafía: {i['silk']})"
                st.selectbox(label, options, index=None, placeholder="Elige…",
                             key=f"sel_{gkey}_{i['num']}")

    b1, b2, _ = st.columns([1, 1, 4])
    if b1.button("✅ Comprobar", type="primary", key=f"check_btn_{gkey}"):
        st.session_state[f"checked_{gkey}"] = True
    if b2.button("🔄 Reiniciar", key=f"reset_btn_{gkey}"):
        reset_game(gkey)
        st.rerun()

    if st.session_state.get(f"checked_{gkey}"):
        answers = {i["num"]: st.session_state.get(f"sel_{gkey}_{i['num']}") for i in items}
        unanswered = [n for n, a in answers.items() if a is None]
        used = [a for a in answers.values() if a is not None]
        correct = sum(1 for i in items if answers[i["num"]] == i["name"])

        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Aciertos", f"{correct} / {len(items)}")
        c2.metric("Nota sobre 10", f"{correct / len(items) * 10:.1f}")
        if correct == len(items):
            st.balloons()
            st.success("¡Perfecto! Has relacionado todo correctamente.")
        if unanswered:
            st.warning("Sin responder: " + ", ".join(f"Nº {n}" for n in unanswered))
        if len(used) != len(set(used)):
            st.info("Has usado algún nombre más de una vez; revisa tus respuestas.")

        with st.expander("Ver resultados detallados", expanded=True):
            for i in items:
                a = answers[i["num"]]
                if a == i["name"]:
                    st.markdown(f"✅ **Nº {i['num']}** · {i['name']}")
                else:
                    st.markdown(
                        f"❌ **Nº {i['num']}** · Tu respuesta: *{a or 'sin responder'}* → "
                        f"Correcto: **{i['name']}**  \n&nbsp;&nbsp;&nbsp;&nbsp;{i['desc']}"
                    )


# ----------------------------------------------------------------- modo pregunta
def mode_quiz(gkey, game, show_hint):
    items = game["items"]
    qk = f"quiz_{gkey}"
    if qk not in st.session_state:
        order = items[:]
        random.shuffle(order)
        st.session_state[qk] = {"order": order, "i": 0, "score": 0, "answered": False, "ok": None}
    s = st.session_state[qk]
    total = len(s["order"])

    col_img, col_q = st.columns([3, 2], gap="large")
    with col_img:
        show_image(game)
    with col_q:
        if s["i"] >= total:
            st.markdown("### 🏁 ¡Terminado!")
            st.metric("Aciertos", f"{s['score']} / {total}")
            st.metric("Nota sobre 10", f"{s['score'] / total * 10:.1f}")
            if s["score"] == total:
                st.balloons()
            if st.button("🔄 Jugar otra vez", type="primary", key=f"again_{gkey}"):
                reset_game(gkey)
                st.rerun()
            return

        item = s["order"][s["i"]]
        st.progress(s["i"] / total, text=f"Pregunta {s['i'] + 1} de {total} · Aciertos: {s['score']}")
        st.markdown(f"### ¿Qué número es…?\n## {item['name']}")
        if show_hint:
            st.caption(f"Pista, serigrafía: {item['silk']}")

        nums = sorted(i["num"] for i in items)
        choice = st.selectbox("Número de la foto", nums, index=None, placeholder="Elige un número…",
                              key=f"choice_{gkey}_{s['i']}", disabled=s["answered"])

        if not s["answered"]:
            if st.button("Responder", type="primary", disabled=choice is None, key=f"answer_{gkey}_{s['i']}"):
                s["answered"] = True
                s["ok"] = choice == item["num"]
                if s["ok"]:
                    s["score"] += 1
                st.rerun()
        else:
            if s["ok"]:
                st.success(f"✅ ¡Correcto! Es el nº {item['num']}.")
            else:
                st.error(f"❌ No. Es el nº {item['num']}.")
            st.info(item["desc"])
            label = "Siguiente ➜" if s["i"] + 1 < total else "Ver resultado"
            if st.button(label, type="primary", key=f"next_{gkey}_{s['i']}"):
                s["i"] += 1
                s["answered"] = False
                s["ok"] = None
                st.rerun()

        if st.button("🔄 Reiniciar", key=f"quiz_reset_{gkey}"):
            reset_game(gkey)
            st.rerun()


# ------------------------------------------------------------------------ main
st.title("🧩 Juego: conoce la placa base")
st.caption("ASRock FM2A68M-DG3+ · Socket FM2+ · chipset AMD A68H")

with st.sidebar:
    st.header("Configuración")
    game_label = st.radio("Juego", [g["title"] for g in GAMES.values()])
    mode = st.radio("Modo", ["Relacionar todo", "¿Qué número es?"])
    hint = st.checkbox("Mostrar pista (serigrafía)", value=False)
    st.divider()
    st.markdown("**Cómo se juega**\n\n- *Relacionar todo*: asigna un nombre a cada número y pulsa Comprobar.\n"
                "- *¿Qué número es?*: te dicen un componente y eliges su número en la foto.")

gkey = next(k for k, g in GAMES.items() if g["title"] == game_label)
game = GAMES[gkey]
st.subheader(game["title"])

if mode == "Relacionar todo":
    mode_match(gkey, game, hint)
else:
    mode_quiz(gkey, game, hint)
