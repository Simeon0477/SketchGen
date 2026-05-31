import './App.css'
import './index.css'
import Generator from './components/Generator/Generator'
import Navbar from './components/Navbar/Navbar'
import Banner from './components/Banner/Banner'

function App() {
  return (
    <>
      <Navbar />
      <Banner />
      <div id='images'>
        <Generator 
          title="Image"
          desc="Décrivez ce que vous imaginez, laissez l'IA faire réaliser vos sketchs."
          cssClass="images-section"
          formAction="/generate_image"
          placeholder="Ex: Une femme souriante"
          type="image"
        />
      </div>
      <div id="videos">
        <Generator 
          title="Vidéo"
          desc="Entrez un prompt, et regardez l'IA animer vos sketchs."
          cssClass="videos-section"
          formAction="/generate_video"
          placeholder="Ex: Un coucher de soleil sur une plage tropicale"
          type="video"
        />
      </div>
    </>
  )
}

export default App