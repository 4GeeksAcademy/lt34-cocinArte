import React, { useContext, useEffect, useState } from "react";
import "../../styles/home.css";
import { Link, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext"

export const Home = () => {
	const [loading, setLoading]=useState(false);
	const [recipesRand, setRecipesRand]=useState([]);
	const { store, actions } = useContext(Context)
	const navigate = useNavigate(); // Importa el hook useNavigate y úsalo aquí

	function navegar() {
		navigate("/categories/create"); // Usa navigate para redirigir programáticamente
	}

	useEffect(()=>{
		recipes_external()
	},[])

	const recipes_external = ()=>{
		setLoading(true);
		fetch('https://api.spoonacular.com/recipes/random?number=12&apiKey=f6c3531069234577afe4d0e2e49fd508',{
			method:'GET',
			headers: { 'Content-Type': 'application/json' }
		}).then(response=>response.json())
		.then(data=>{setRecipesRand(data.recipes || []); console.log(data.recipes)})
		.finally(() => setLoading(false))
	}

	return (
        <div className="container text-center mt-5">
            <h1 className="container d-flex justify-content-center">Hola Cocinero!</h1>
            {loading ? (
                <h1 className="container text-center text-danger">Loading</h1>
            ):(
                <div className="container-fluid d-flex row ">
                    {recipesRand.length > 0 ? recipesRand.map((recipe)=>(
                        <div key={recipe.id} className="card align-items-stretch m-2 col-3" style={{ width:"18rem" }}>
                            <img src={recipe.image} className="card-img-top" alt={recipe.title} />
                            <div className="card-body d-flex flex-column">
                                <h5 className="card-title">{recipe.title}</h5>
                                <p className="card-text">{recipe.creditsText}</p>
                                <Link className="mt-auto" to={`/recipe/api/${recipe.id}`}><button>Quiero probarla!</button></Link>
                            </div>
                        </div>
                    )):(
                        <h1 className="container text-center text-danger">Error al cargar recetas.</h1>
                    )}
                </div>
            )}
            <p>
                This boilerplate comes with lots of documentation:{" "}
                <a href="https://start.4geeksacademy.com/starters/react-flask">
                    Read documentation
                </a>
            </p>
			{store.authadmin ? (
                <button onClick={navegar}> {/* Llama a la función de navegación aquí */}
                    Crear etiquetas!
                </button>
            ) : null}
        </div>
    )
}