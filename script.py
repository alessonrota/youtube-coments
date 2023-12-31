pip install --upgrade google-api-python-client

from googleapiclient.discovery import build
import pandas as pd

# Defina sua chave de API aqui
api_key = 'INSIRA A CHAVE API AQUI'

# Inicializa o cliente da API do YouTube
youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_comments(video_id, max_results=100):
    # Coleta os comentários de um vídeo específico
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=max_results
    ).execute()

    comments_data = []
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments_data.append({
                'author': comment['authorDisplayName'],
                'comment': comment['textDisplay'],
                'likes': comment['likeCount'],
                'published_at': comment['publishedAt']
            })

        # Verifica se existe próxima página
        if 'nextPageToken' in results:
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=results['nextPageToken'],
                maxResults=max_results
            ).execute()
        else:
            break

    return comments_data

# Substitua 'VIDEO_ID' pelo ID do vídeo do qual você deseja obter os comentários
video_id = 'hzUvn-KolrQ'
comments_data = get_video_comments(video_id)

# Cria um DataFrame com os dados
df = pd.DataFrame(comments_data)

# Salva o DataFrame como um arquivo CSV
df.to_csv('comentarios_youtube.csv', index=False)

# Imprime as primeiras linhas do DataFrame para verificação
print(df.head())
