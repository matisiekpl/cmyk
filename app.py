import streamlit as st
from PIL import Image
import numpy as np


def rgb_to_cmyk(i):
    np_image = np.array(i.convert('RGB')) / 255.0
    k = 1 - np.max(np_image, axis=2)
    c = (1 - np_image[..., 0] - k) / (1 - k + 1e-10)
    m = (1 - np_image[..., 1] - k) / (1 - k + 1e-10)
    y = (1 - np_image[..., 2] - k) / (1 - k + 1e-10)
    c[np.isnan(c)] = 0
    m[np.isnan(m)] = 0
    y[np.isnan(y)] = 0
    return c, m, y, k


def calculate_ink_cost(c, m, y, k, cost_c, cost_m, cost_y, cost_k):
    total_c = np.sum(c)
    total_m = np.sum(m)
    total_y = np.sum(y)
    total_k = np.sum(k)
    return (total_c * cost_c + total_m * cost_m + total_y * cost_y + total_k * cost_k) / c.size


st.title("Obliczanie kosztu tuszu druku CMYK")

uploaded_file = st.file_uploader("Wybierz plik JPG", type=("jpg", "jpeg", "png"))

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Wczytany obraz", use_column_width=True)

    C, M, Y, K = rgb_to_cmyk(image)

    st.write("Średnie użycie tuszu w kanale C:", np.mean(C))
    st.write("Średnie użycie tuszu w kanale M:", np.mean(M))
    st.write("Średnie użycie tuszu w kanale Y:", np.mean(Y))
    st.write("Średnie użycie tuszu w kanale K:", np.mean(K))

    cost_c = st.number_input("Koszt tuszu C na jednostkę", value=1)
    cost_m = st.number_input("Koszt tuszu M na jednostkę", value=1)
    cost_y = st.number_input("Koszt tuszu Y na jednostkę", value=1)
    cost_k = st.number_input("Koszt tuszu K na jednostkę", value=1)

    if st.button("Oblicz koszt"):
        total_cost = calculate_ink_cost(C, M, Y, K, cost_c, cost_m, cost_y, cost_k)
        st.write(f"Koszt tuszu to: {total_cost}")
