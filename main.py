from pytube import YouTube
import streamlit as st


def formatoMinutos(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    return f"{horas:02}:{minutos:02}:{segundos:02}"


def barraProgreso(stream=None, chunk=None, bytes_remaining=None):
    total_size = stream.filesize / 1000000
    bytes_downloaded = total_size - (bytes_remaining / 1000000)
    st.progress(bytes_downloaded / total_size)


# Título de la app
st.title("YouTube Video Downloader")

# Subtitulo de la app
st.subheader("Download any YouTube video in any resolution")

# Obtener el link del usuario
link = st.text_input("Enter the link of the YouTube video")

# Validar que el link no esté vacío
if link:
    yt = YouTube(link, on_progress_callback=barraProgreso)
    st.write("Title:", yt.title)

    # Centrar imágen

    row1 = st.empty()
    row1col1, row1col2, row1col3 = row1.columns(3)
    row1col1.empty()
    row1col2.image(yt.thumbnail_url)
    row1col3.empty()

    st.write("Number of views:", yt.views)
    st.write(f"Length of video: {formatoMinutos(yt.length)}")

    no = st.empty()
    no.text("Getting available resolutions...")
    arrei = yt.streams.asc()
    no.empty()

    opciones = [
        f'{i.resolution} - {i.mime_type} - {i.filesize / 1000000:.1f} MB'
        for i in arrei
    ]

    choice = st.selectbox("Select the resolution", opciones)
    if choice:
        botonConf = st.button("Download")
        if botonConf:
            placeholder = st.empty()
            yt = arrei[opciones.index(choice)]
            placeholder.text("Downloading...")
            yt.download()
            placeholder.text("Download completed!!")
