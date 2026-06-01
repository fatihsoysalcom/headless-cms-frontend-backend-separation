# Headless CMS Frontend Backend Separation

This example demonstrates the core concept of Headless CMS architecture: the separation of frontend and backend. A single Python script acts as a minimal backend, serving content via a `/api/content` JSON endpoint, and also as a simple frontend, serving an HTML page with JavaScript that fetches and displays this content. It illustrates how the content (backend) is decoupled from its presentation (frontend).

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Run the script from your terminal: `python main.py`
3. Open your web browser and navigate to `http://localhost:8000` to see the frontend consuming the API.

## Original Article

This example accompanies the Turkish article: [Headless CMS Mimarisi: Frontend ve Backend Ayrımını Anlamak](https://fatihsoysal.com/blog/headless-cms-mimarisi-frontend-ve-backend-ayrimini-anlamak/).

## License

MIT — see [LICENSE](LICENSE).
