import streamlit as st
import yt_dlp
import os
import tempfile
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="YouTube Downloader PRO",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stDownloadButton button {
        width: 100%;
        background-color: #2B7A0B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
        font-weight: 700;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎬 YouTube Downloader")
    st.markdown("---")
    
    st.markdown("""
    ### 📊 Sobre
    
    **Versão:** 3.0 Web
    
    **Plataformas suportadas:**
    - ✅ YouTube
    - ✅ TikTok
    - ✅ Instagram
    - ✅ Twitter/X
    - ✅ Facebook
    - ✅ Vimeo
    - ✅ E +1000 sites!
    
    **Formatos:**
    - 🎵 MP3 (áudio 320kbps)
    - 🎥 MP4 (várias qualidades)
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ### ⚠️ Avisos
    
    - Vídeos privados não funcionam
    - Respeite direitos autorais
    - Apenas conteúdo público
    - Uso pessoal apenas
    """)
    
    st.markdown("---")
    st.caption("Feito com ❤️ usando Streamlit")

# Header
st.title("🎬 YouTube Downloader PRO")
st.markdown("### Baixe vídeos e áudios de mais de 1000 plataformas!")

st.markdown("---")

# Área principal
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "🔗 Cole o link do vídeo aqui:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Funciona com YouTube, TikTok, Instagram, Twitter e mais!"
    )

with col2:
    formato = st.selectbox(
        "📝 Formato:",
        ["MP3", "MP4"],
        help="MP3 = apenas áudio | MP4 = vídeo completo"
    )

# Seletor de qualidade (só para MP4)
if formato == "MP4":
    qualidade = st.select_slider(
        "🎬 Qualidade do vídeo:",
        options=["360p", "480p", "720p (HD)", "1080p (Full HD)", "1440p (2K)", "2160p (4K)", "Melhor disponível"],
        value="1080p (Full HD)",
        help="Maior qualidade = arquivo maior e download mais demorado"
    )
else:
    qualidade = None
    st.info("🎵 **MP3:** Áudio sempre baixado na melhor qualidade (320kbps)")

st.markdown("---")

# Função de download
def baixar_video(url, formato, qualidade):
    """Baixa o vídeo/áudio e retorna o arquivo"""
    
    # Cria diretório temporário
    temp_dir = tempfile.mkdtemp()
    
    # Configurações do yt-dlp - ULTRA BYPASS MODE
    opcoes = {
    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
    
    # 🔥 BYPASS AGRESSIVO
    'age_limit': None,
    'geo_bypass': True,
    'geo_bypass_country': 'US',
    
    # 🔥 Headers completos de navegador real
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    },

    # 🔥 Tenta TODOS os métodos possíveis
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web', 'ios', 'mweb'],
            'player_skip': ['webpage', 'configs'],
            'skip': ['hls', 'dash'],
        }
    },
    
    # 🔥 Outras tentativas
    'nocheckcertificate': True,
    'prefer_insecure': True,
}
    
    # Configurações específicas por formato
    if formato == "MP3":
        opcoes.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
        extensao = 'mp3'
    else:
        # MP4 com qualidade selecionada
        if qualidade and qualidade != "Melhor disponível":
            resolucao = qualidade.split('p')[0]
            opcoes.update({
                'format': f'best[height<={resolucao}]',

                'merge_output_format': 'mp4',
            })
        else:
            opcoes.update({
                'format': 'best',
                'merge_output_format': 'mp4',
            })
        extensao = 'mp4'
    
    # Baixa o vídeo
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'video')
        
        # Encontra o arquivo baixado
        for arquivo in os.listdir(temp_dir):
            if arquivo.endswith(f'.{extensao}'):
                caminho_completo = os.path.join(temp_dir, arquivo)
                return caminho_completo, titulo
    
    return None, None

# Botão de download
if st.button("⬇️ BAIXAR AGORA", type="primary", use_container_width=True):
    if not url:
        st.error("❌ Por favor, cole um link válido!")
    else:
        try:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Analisando link...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text("📥 Baixando arquivo...")
            progress_bar.progress(40)
            
            # Faz o download
            caminho_arquivo, titulo = baixar_video(url, formato, qualidade)
            
            progress_bar.progress(80)
            status_text.text("✅ Processando...")
            time.sleep(0.3)
            
            progress_bar.progress(100)
            status_text.text("🎉 Download concluído!")
            
            if caminho_arquivo and os.path.exists(caminho_arquivo):
                # Lê o arquivo
                with open(caminho_arquivo, 'rb') as f:
                    arquivo_bytes = f.read()
                
                # Mostra informações
                tamanho_mb = len(arquivo_bytes) / (1024 * 1024)
                
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Download Pronto!</h3>
                    <p><strong>📄 Título:</strong> {titulo}</p>
                    <p><strong>📝 Formato:</strong> {formato}</p>
                    {f'<p><strong>🎬 Qualidade:</strong> {qualidade}</p>' if formato == 'MP4' else ''}
                    <p><strong>📦 Tamanho:</strong> {tamanho_mb:.1f} MB</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botão de download
                nome_arquivo = f"{titulo}.{formato.lower()}"
                st.download_button(
                    label=f"📥 BAIXAR {formato} ({tamanho_mb:.1f} MB)",
                    data=arquivo_bytes,
                    file_name=nome_arquivo,
                    mime=f"{'audio' if formato == 'MP3' else 'video'}/{formato.lower()}",
                    use_container_width=True
                )
                
                # Limpa arquivo temporário
                try:
                    os.remove(caminho_arquivo)
                    os.rmdir(os.path.dirname(caminho_arquivo))
                except:
                    pass
                
            else:
                st.error("❌ Erro ao processar o arquivo. Tente novamente.")
                
        except Exception as e:
            erro_msg = str(e)
            
            # Erros específicos
            if "private" in erro_msg.lower():
                st.error("❌ Este vídeo é privado e não pode ser baixado.")
            elif "age" in erro_msg.lower() or "restricted" in erro_msg.lower():
                st.error("❌ Este vídeo tem restrição de idade (+18) e não pode ser baixado.")
            elif "not available" in erro_msg.lower():
                st.error("❌ Este vídeo não está disponível ou foi removido.")
            elif "unsupported url" in erro_msg.lower():
                st.error("❌ Este site não é suportado. Tente YouTube, TikTok, Instagram ou Twitter.")
            else:
                st.error(f"❌ Erro ao baixar: {erro_msg}")

# Informações adicionais
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4>🎥 Qualidade MP4</h4>
        <p><strong>4K/2K:</strong> Máxima qualidade (1-5GB)</p>
        <p><strong>1080p:</strong> Full HD (500MB-2GB)</p>
        <p><strong>720p:</strong> HD (200-800MB)</p>
        <p><strong>480p/360p:</strong> Rápido e leve</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>🎵 Qualidade MP3</h4>
        <p><strong>320kbps:</strong> Melhor qualidade</p>
        <p><strong>Extraído do vídeo original</strong></p>
        <p><strong>Tamanho:</strong> ~3-5MB por minuto</p>
        <p><strong>Compatível com tudo</strong></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ Limitações</h4>
        <p>❌ Conteúdo privado</p>
        <p>❌ Lives ao vivo</p>
        <p>❌ Playlists (só 1 vídeo)</p>
        <p>✅ Apenas conteúdo público</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 2rem;">
    <p><strong>YouTube Downloader PRO</strong> - Versão Web 3.0</p>
    <p>Feito com ❤️ usando Python, Streamlit e yt-dlp</p>
    <p>⚖️ Use com responsabilidade - Respeite os direitos autorais</p>
</div>
""", unsafe_allow_html=True)
