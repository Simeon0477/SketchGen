import { useState } from "react";
import "./Generator.css";

export interface GeneratorProps {
  title: string;
  desc: string;
  cssClass: string;
  formAction: string;
  placeholder: string;
  type: "image" | "video";
}

function Generator({ title, desc, cssClass, placeholder, type }: GeneratorProps) {
  const [prompt, setPrompt]     = useState("");
  const [result, setResult]     = useState<string | null>(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const endpoint = type === "image" ? "/generate_image" : "/generate_video";
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({prompt}),
      });

      if (!response.ok) throw new Error(`Erreur serveur : ${response.status}`);

      const data = await response.json();
      setResult(type === "image" ? data.image : data.video);

    } catch (err: any) {
      setError(err.message || "Une erreur est survenue");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className={cssClass}>
      <div className="content">
        <h2>{title}</h2>
        <p className="section-desc">{desc}</p>

        <form onSubmit={handleSubmit}>
          <div className="input-wrap">
            <input
              type="text"
              name="prompt"
              placeholder={placeholder}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Génération..." : "Générer"}
            </button>
          </div>
        </form>

        {/* Loader */}
        {loading && (
          <div className="loader-wrap">
            <div className="loader" />
            <p>{type === "image" ? "Génération de l'image..." : "Génération de la vidéo..."}</p>
          </div>
        )}

        {/* Erreur */}
        {error && (
          <div className="error-wrap">
            <p>{error}</p>
          </div>
        )}

        {/* Résultat image */}
        {result && type === "image" && (
          <div className="result-wrap">
            <img
              src={`data:image/png;base64,${result}`}
              alt="Image générée"
              className="result-image"
            />
            <a
              href={`data:image/png;base64,${result}`}
              download="sketch.png"
              className="download-btn"
            >
              Télécharger
            </a>
          </div>
        )}

        {/* Résultat vidéo */}
        {result && type === "video" && (
          <div className="result-wrap">
            <img
              src={`data:image/gif;base64,${result}`}
              alt="Vidéo générée"
              className="result-image"
            />
            <a
              href={`data:image/gif;base64,${result}`}
              download="sketch.gif"
              className="download-btn"
            >
              Télécharger
            </a>
          </div>
        )}
      </div>
    </section>
  );
}

export default Generator;