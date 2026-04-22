"""
Extractor de datos de Instagram usando RapidAPI (Instagram Scraper Stable API)
Materia: Dispositivos Móviles
"""

import requests
import json
import csv
import os
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================
API_KEY         = "fb198fbceemsh56adb1f41201b13p1db91djsn209e7fa53df8"
PERFIL_OBJETIVO = "enchufetv"
MAX_POSTS       = 15
# ============================================================

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "instagram-scraper-stable-api.p.rapidapi.com",
    "Content-Type": "application/x-www-form-urlencoded"
}


def extraer_perfil(username):
    print("👤 Extrayendo datos del perfil...")
    url = "https://instagram-scraper-stable-api.p.rapidapi.com/ig_get_fb_profile.php"
    payload = {
        "username_or_url": username,
        "data": "basic"
    }

    response = requests.post(url, headers=HEADERS, data=payload)
    response.raise_for_status()
    data = response.json()

    perfil = {
        "username": data.get("username"),
        "nombre_completo": data.get("full_name"),
        "biografia": data.get("biography"),
        "url_biografia": data.get("external_url"),
        "seguidores": data.get("edge_followed_by", {}).get("count", 0),
        "seguidos": data.get("edge_follow", {}).get("count", 0),
        "total_publicaciones": data.get("edge_owner_to_timeline_media", {}).get("count", 0),
        "es_verificado": data.get("is_verified"),
        "es_privado": data.get("is_private"),
        "es_negocio": data.get("is_business_account"),
        "categoria_negocio": data.get("business_category_name"),
        "url_foto_perfil": data.get("profile_pic_url"),
        "id_usuario": str(data.get("id", "")),
        "fecha_extraccion": datetime.now().isoformat(),
    }

    print("✅ Perfil extraído:")
    print(f"   • Nombre:        {perfil['nombre_completo']}")
    print(f"   • Seguidores:    {perfil['seguidores']:,}")
    print(f"   • Seguidos:      {perfil['seguidos']:,}")
    print(f"   • Publicaciones: {perfil['total_publicaciones']:,}")
    print(f"   • Verificado:    {perfil['es_verificado']}")

    return perfil


def extraer_posts(username, max_posts):
    print(f"\n📸 Extrayendo últimos {max_posts} posts...")
    url = "https://instagram-scraper-stable-api.p.rapidapi.com/get_ig_user_posts.php"
    payload = {
        "username_or_url": username,
        "pagination_token": "",
        "amount": str(max_posts)
    }

    response = requests.post(url, headers=HEADERS, data=payload)
    response.raise_for_status()
    items = response.json()

    if isinstance(items, dict):
        items = items.get("data", items.get("posts", items.get("items", [])))

    lista_posts = []

    for i, m in enumerate(items[:max_posts]):
        node = m.get("node", m)

        caption_text = ""
        caption_edges = node.get("edge_media_to_caption", {}).get("edges", [])
        if caption_edges:
            caption_text = caption_edges[0].get("node", {}).get("text", "") or ""

        timestamp = node.get("taken_at_timestamp", node.get("taken_at", 0))

        post = {
            "shortcode": node.get("shortcode"),
            "url_post": f"https://www.instagram.com/p/{node.get('shortcode')}/",
            "tipo": "video" if node.get("is_video") else "imagen",
            "descripcion": caption_text,
            "likes": node.get("edge_liked_by", {}).get("count", node.get("like_count", 0)),
            "comentarios": node.get("edge_media_to_comment", {}).get("count", node.get("comment_count", 0)),
            "visualizaciones": node.get("video_view_count", 0),
            "fecha_publicacion": datetime.fromtimestamp(timestamp).isoformat() if timestamp else "",
            "hashtags": [w for w in caption_text.split() if w.startswith("#")],
            "menciones": [w for w in caption_text.split() if w.startswith("@")],
        }

        lista_posts.append(post)
        print(f"   Post {i+1}: {post['fecha_publicacion'][:10]} | ❤️ {post['likes']:,} | 💬 {post['comentarios']:,}")

    return lista_posts


def guardar_resultados(perfil, posts, username):
    estadisticas = {
        "posts_extraidos": len(posts),
        "promedio_likes": round(sum(p["likes"] for p in posts) / max(len(posts), 1), 2),
        "promedio_comentarios": round(sum(p["comentarios"] for p in posts) / max(len(posts), 1), 2),
        "total_likes": sum(p["likes"] for p in posts),
        "total_comentarios": sum(p["comentarios"] for p in posts),
    }

    resultado = {
        "perfil": perfil,
        "publicaciones": posts,
        "estadisticas": estadisticas
    }

    carpeta = f"output_{username}"
    os.makedirs(carpeta, exist_ok=True)

    with open(f"{carpeta}/{username}_datos.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\n💾 JSON guardado en: {carpeta}/{username}_datos.json")

    if posts:
        with open(f"{carpeta}/{username}_posts.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=posts[0].keys())
            writer.writeheader()
            writer.writerows(posts)
        print(f"💾 Posts CSV guardado en: {carpeta}/{username}_posts.csv")

    with open(f"{carpeta}/{username}_perfil.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=perfil.keys())
        writer.writeheader()
        writer.writerow(perfil)
    print(f"💾 Perfil CSV guardado en: {carpeta}/{username}_perfil.csv")

    print("\n📊 Estadísticas:")
    print(f"   • Posts extraídos:      {estadisticas['posts_extraidos']}")
    print(f"   • Promedio likes:       {estadisticas['promedio_likes']:,}")
    print(f"   • Promedio comentarios: {estadisticas['promedio_comentarios']:,}")
    print(f"   • Total likes:          {estadisticas['total_likes']:,}")


def main():
    print(f"\n{'='*50}")
    print(f"  Extrayendo datos de: @{PERFIL_OBJETIVO}")
    print("  Método: RapidAPI - Instagram Scraper Stable API")
    print(f"{'='*50}\n")

    try:
        perfil = extraer_perfil(PERFIL_OBJETIVO)
        posts = extraer_posts(PERFIL_OBJETIVO, MAX_POSTS)
        guardar_resultados(perfil, posts, PERFIL_OBJETIVO)

        print("\n✅ ¡Extracción completada exitosamente!")
        print(f"   Revisa la carpeta: output_{PERFIL_OBJETIVO}/")

    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP: {e}")
        print("   Revisa la API Key o los parámetros enviados.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
