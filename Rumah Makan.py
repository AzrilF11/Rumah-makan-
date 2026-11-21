from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(
    page_title="Warung Nasi Lumbung Lambung GLC",
    page_icon="🍚",
    layout="wide",
    initial_sidebar_state="expanded",
)


ROOT = Path(__file__).parent
IMAGE_DIR = ROOT / "public" / "images"
ADDRESS = (
    "Ruko CBD Greenlake Blok L No. 7, RT.006/RW.003, Ketapang, "
    "Kec. Cipondoh, Kota Tangerang, Banten 15158"
)
PHONE = "6287775267898"


@dataclass(frozen=True)
class MenuItem:
    name: str
    description: str
    category: str
    price: int
    image: str | Path


MENU = [
    MenuItem(
        "Nasi Jeruk Ayam Pedas",
        "Nasi jeruk, ayam suwir pedas, telur, dan sambal.",
        "Nasi",
        38_000,
        "https://images.unsplash.com/photo-1666239308347-4292ea2ff777"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Baso Lohoa Komplit",
        "Kuah hangat, baso lohoa, sayuran, dan bawang goreng.",
        "Berkuah",
        32_000,
        "https://images.unsplash.com/photo-1707271914006-627b89038143"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Nasi Oncom Leunca",
        "Oncom leunca, bakwan sayur, dan lalapan segar.",
        "Nasi",
        28_000,
        "https://images.unsplash.com/photo-1694111133919-e365928cc252"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Nasi Ayam Serundeng",
        "Ayam goreng, serundeng kelapa, tahu, dan sambal merah.",
        "Nasi",
        36_000,
        "https://images.unsplash.com/photo-1586511930877-d20ef1e5d3c6"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Nasi Daging Sambal Ijo",
        "Daging empuk, sambal hijau, tumis buncis, dan kerupuk.",
        "Nasi",
        45_000,
        "https://images.unsplash.com/photo-1630315500315-43112e2bfd88"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Soto Ayam Kampung",
        "Soto bening, ayam kampung, kol, soun, dan perkedel.",
        "Berkuah",
        34_000,
        "https://images.unsplash.com/photo-1687419950105-b1cdeb6c66bc"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Bakwan Sayur",
        "Bakwan renyah dengan wortel, kol, dan daun bawang.",
        "Camilan",
        15_000,
        IMAGE_DIR / "bakwan-sayur.jpg",
    ),
    MenuItem(
        "Tahu Isi Pedas",
        "Tahu goreng berisi sayuran dengan cabai rawit.",
        "Camilan",
        18_000,
        "https://images.unsplash.com/photo-1762305194201-077e7e23ccf2"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Es Teh Lemon",
        "Teh melati, lemon segar, dan gula aren.",
        "Minuman",
        12_000,
        IMAGE_DIR / "es-teh-lemon.png",
    ),
    MenuItem(
        "Es Jeruk Peras",
        "Jeruk peras segar dengan pilihan gula normal atau sedikit.",
        "Minuman",
        15_000,
        "https://images.unsplash.com/photo-1600271886742-f049cd451bba"
        "?auto=format&fit=crop&w=900&q=85",
    ),
    MenuItem(
        "Kopi Susu Gula Aren",
        "Espresso, susu segar, dan gula aren.",
        "Minuman",
        18_000,
        IMAGE_DIR / "kopi-susu-gula-aren.png",
    ),
]


def rupiah(value: int) -> str:
    return f"Rp{value:,.0f}".replace(",", ".")


def menu_by_name(name: str) -> MenuItem:
    return next(item for item in MENU if item.name == name)


def add_to_cart(name: str) -> None:
    st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1


def change_quantity(name: str, change: int) -> None:
    quantity = st.session_state.cart.get(name, 0) + change
    if quantity <= 0:
        st.session_state.cart.pop(name, None)
    else:
        st.session_state.cart[name] = quantity


def whatsapp_url(order_type: str, note: str) -> str:
    lines = ["Halo Warung Nasi Lumbung Lambung GLC, saya ingin memesan:", ""]
    total = 0
    for name, quantity in st.session_state.cart.items():
        item = menu_by_name(name)
        subtotal = item.price * quantity
        total += subtotal
        lines.append(f"• {quantity}x {name} — {rupiah(subtotal)}")
    lines.extend(["", f"Tipe pesanan: {order_type}"])
    if note.strip():
        lines.append(f"Catatan: {note.strip()}")
    lines.extend(
        [
            f"Total: {rupiah(total)}",
            "",
            "Mohon konfirmasi ketersediaan dan waktu pesanan. Terima kasih.",
        ]
    )
    return f"https://wa.me/{PHONE}?text={quote(chr(10).join(lines))}"


if "cart" not in st.session_state:
    st.session_state.cart = {}
if "reviews" not in st.session_state:
    st.session_state.reviews = [
        {
            "name": "Cva Cavalera",
            "rating": 5,
            "text": "Menunya segar, tempatnya bersih, dan harganya masih oke. BEST!",
        },
        {
            "name": "Deren Firdaus",
            "rating": 5,
            "text": "Makanan enak, comfort food, harga murah. Sudah langganan terus!",
        },
    ]


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display&display=swap');
    :root {
        --forest: #294c37;
        --forest-deep: #173524;
        --cream: #f7f4ec;
        --paper: #fffdf8;
        --clay: #b5573f;
        --muted: #71776f;
        --line: #dedfd7;
    }
    .stApp { background: var(--paper); color: #1c261d; font-family: "DM Sans", sans-serif; }
    .block-container { max-width: 1220px; padding-top: 2.5rem; padding-bottom: 5rem; }
    h1, h2, h3 { font-family: "DM Serif Display", serif !important; font-weight: 400 !important; }
    h1 { font-size: clamp(3rem, 6vw, 5.6rem) !important; line-height: .95 !important; letter-spacing: -.04em; }
    h2 { font-size: 2.6rem !important; }
    [data-testid="stSidebar"] { background: var(--cream); border-left: 1px solid var(--line); }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }
    .eyebrow { color: var(--clay); text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; font-weight: 700; }
    .meta { color: var(--muted); font-size: .95rem; margin: .8rem 0 1.4rem; }
    .meta strong { color: var(--forest); }
    .service { padding: .9rem 1.1rem; border: 1px solid var(--line); background: var(--cream); color: var(--forest); }
    .menu-category { color: var(--clay); text-transform: uppercase; letter-spacing: .1em; font-size: .65rem; font-weight: 700; }
    .menu-title { font-family: "DM Serif Display"; font-size: 1.35rem; margin: .35rem 0; min-height: 3.1rem; }
    .menu-detail { color: var(--muted); font-size: .78rem; line-height: 1.5; min-height: 3.5rem; }
    .price { color: var(--forest); font-weight: 700; margin-bottom: .5rem; }
    .review-card { border-bottom: 1px solid var(--line); padding: 1rem 0; }
    .review-card strong { color: var(--forest); }
    .review-card p { color: #454b45; font-size: .9rem; }
    .info-box { border: 1px solid var(--line); padding: 1.25rem; background: white; min-height: 9rem; }
    .info-box span { color: var(--muted); font-size: .8rem; line-height: 1.5; }
    .stars { color: #dfa72e; letter-spacing: .1em; }
    .cart-total { border-top: 1px solid var(--line); margin-top: 1rem; padding-top: 1rem; font-size: 1.15rem; }
    div.stButton > button, div.stLinkButton > a {
        border-radius: 999px; border-color: var(--forest); font-weight: 700;
    }
    div.stButton > button:hover, div.stLinkButton > a:hover {
        border-color: var(--forest-deep); color: var(--forest-deep);
    }
    [data-testid="stImage"] img { border-radius: .2rem; object-fit: cover; }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## Pesanan Anda")
    if not st.session_state.cart:
        st.caption("Keranjang masih kosong. Tambahkan menu favorit Anda.")
    else:
        total = 0
        for item_name, quantity in list(st.session_state.cart.items()):
            item = menu_by_name(item_name)
            subtotal = item.price * quantity
            total += subtotal
            st.markdown(f"**{item.name}**")
            st.caption(f"{quantity} × {rupiah(item.price)} = {rupiah(subtotal)}")
            minus, count, plus = st.columns([1, 1, 1])
            minus.button("−", key=f"minus-{item.name}", on_click=change_quantity, args=(item.name, -1))
            count.markdown(f"<div style='text-align:center;padding:.35rem'>{quantity}</div>", unsafe_allow_html=True)
            plus.button("+", key=f"plus-{item.name}", on_click=change_quantity, args=(item.name, 1))
        st.markdown(f"<div class='cart-total'>Total <strong>{rupiah(total)}</strong></div>", unsafe_allow_html=True)
        order_type = st.radio("Pesanan untuk", ["Bawa pulang", "Makan di tempat"])
        order_note = st.text_area("Catatan untuk dapur", placeholder="Contoh: sambal dipisah")
        st.link_button(
            "Pesan via WhatsApp",
            whatsapp_url(order_type, order_note),
            use_container_width=True,
            type="primary",
        )
        st.caption("Pesanan akan dikonfirmasi langsung oleh pihak warung.")


hero_copy, hero_image = st.columns([1.05, 1], gap="large", vertical_alignment="center")
with hero_copy:
    st.markdown("<div class='eyebrow'>Pilihan warga Cipondoh</div>", unsafe_allow_html=True)
    st.title("Warung Nasi Lumbung Lambung GLC")
    st.markdown(
        "<div class='meta'><strong>4,9 ★★★★★</strong> &nbsp; 208 ulasan &nbsp;·&nbsp; Rp25–50 rb</div>",
        unsafe_allow_html=True,
    )
    st.write("Masakan rumahan yang hangat, jujur, dan selalu bikin ingin kembali.")
    directions_url = (
        "https://www.google.com/maps/dir/?api=1&destination=" + quote(ADDRESS)
    )
    st.link_button("Buka petunjuk arah", directions_url, type="primary")
with hero_image:
    st.image(
        "https://images.unsplash.com/photo-1584455486010-760bd0b28fc2"
        "?auto=format&fit=crop&w=1200&q=85",
        caption="Masakan rumahan khas Indonesia",
        use_container_width=True,
    )

st.markdown("---")
service_cols = st.columns(3)
for column, text in zip(
    service_cols,
    ["✓ Makan di tempat", "✓ Bawa pulang", "✓ Halal"],
):
    column.markdown(f"<div class='service'>{text}</div>", unsafe_allow_html=True)

overview_tab, menu_tab, reviews_tab = st.tabs(["Ringkasan", "Semua Menu", "Ulasan"])

with overview_tab:
    st.markdown("## Informasi warung")
    info_columns = st.columns(3)
    info_columns[0].markdown(
        f"<div class='info-box'><b>📍 Lokasi</b><br><span>{ADDRESS}</span></div>",
        unsafe_allow_html=True,
    )
    info_columns[1].markdown(
        "<div class='info-box'><b>◷ Jam buka</b><br><span>Buka hari ini<br>Tutup pukul 20.00</span></div>",
        unsafe_allow_html=True,
    )
    info_columns[2].markdown(
        "<div class='info-box'><b>☎ Telepon</b><br><span>0877-7526-7898<br>Rp25.000–50.000/orang</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Menu favorit")
    favorite_columns = st.columns(3)
    for column, item in zip(favorite_columns, MENU[:3]):
        with column:
            st.image(str(item.image), use_container_width=True)
            st.markdown(f"<div class='menu-title'>{item.name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>{rupiah(item.price)}</div>", unsafe_allow_html=True)
            st.button(
                "Tambah ke pesanan",
                key=f"favorite-{item.name}",
                on_click=add_to_cart,
                args=(item.name,),
                use_container_width=True,
            )

with menu_tab:
    st.markdown("## Semua menu")
    selected_category = st.segmented_control(
        "Kategori",
        ["Semua", "Nasi", "Berkuah", "Camilan", "Minuman"],
        default="Semua",
    )
    filtered_menu = (
        MENU
        if selected_category in (None, "Semua")
        else [item for item in MENU if item.category == selected_category]
    )
    for start in range(0, len(filtered_menu), 3):
        columns = st.columns(3)
        for column, item in zip(columns, filtered_menu[start : start + 3]):
            with column:
                st.image(str(item.image), use_container_width=True)
                st.markdown(f"<div class='menu-category'>{item.category}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='menu-title'>{item.name}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='menu-detail'>{item.description}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price'>{rupiah(item.price)}</div>", unsafe_allow_html=True)
                st.button(
                    "Tambah",
                    key=f"menu-{item.name}",
                    on_click=add_to_cart,
                    args=(item.name,),
                    use_container_width=True,
                )

with reviews_tab:
    summary, form_column = st.columns([1.15, 1], gap="large")
    with summary:
        st.markdown("## Ulasan pelanggan")
        st.markdown("<div class='stars'>★★★★★ &nbsp; <b>4,9</b></div>", unsafe_allow_html=True)
        st.caption(f"{208 + max(0, len(st.session_state.reviews) - 2)} ulasan")
        for review in st.session_state.reviews:
            stars = "★" * review["rating"] + "☆" * (5 - review["rating"])
            st.markdown(
                f"""
                <div class="review-card">
                    <strong>{escape(review["name"])}</strong>
                    <div class="stars">{stars}</div>
                    <p>{escape(review["text"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with form_column:
        st.markdown("## Tulis ulasan")
        with st.form("review-form", clear_on_submit=True):
            name = st.text_input("Nama Anda")
            rating = st.feedback("stars")
            review_text = st.text_area(
                "Ceritakan pengalaman Anda",
                max_chars=500,
                height=140,
            )
            submitted = st.form_submit_button("Kirim ulasan", use_container_width=True)
            if submitted:
                if name.strip() and review_text.strip() and rating is not None:
                    st.session_state.reviews.insert(
                        0,
                        {
                            "name": name.strip(),
                            "rating": rating + 1,
                            "text": review_text.strip(),
                        },
                    )
                    st.success("Terima kasih. Ulasan Anda sudah ditambahkan.")
                else:
                    st.error("Lengkapi nama, rating, dan ulasan Anda.")
