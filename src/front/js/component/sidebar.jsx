import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export function Sidebar(){
    const [categories, setCategories] = useState([])
    useEffect(()=>{
        fetch(process.env.BACKEND_URL + '/api/categorias',{ 
			method: 'GET', 
			headers: { 'Content-Type': 'application/json' } 
		}) 
		.then(response=> response.json()) 
		.then(data=> setCategories(data));
    },[])
    fetch(process.env.BACKEND_URL + '/api/categorias',{ 
        method: 'GET', 
        headers: { 'Content-Type': 'application/json' } 
    }) 
    .then(response=> response.json()) 
    .then(data=> setCategories(data));
    return(
        <div className="flex-shrink-0 p-3 bg-light vh-100" style={{width: '280px'}}>
            <a href="/" className="d-flex align-items-center pb-3 mb-3 link-body-emphasis text-decoration-none border-bottom">
                <svg className="bi pe-none me-2" width="30" height="24"><use href="#bootstrap"></use></svg>
                <span className="fs-5 fw-semibold">cocinArte</span>
            </a>
            <ul className="list-unstyled ps-0">
                <li className="mb-1">
                    <button className="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#home-collapse" aria-expanded="true">Home</button>
                    <div className="collapse show" id="home-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><Link className="dropdown-item" to="/recipe/">Ver Recetas!</Link></li>
                        </ul>
                    </div>
                </li>
                <li className="mb-1">
                    <button className="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false">Categorias</button>
                    <div className="collapse" id="dashboard-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                        {categories.map((category) => (
								<li key={category.id}> 
									<Link className="dropdown-item" to={`/category/search/${category.id}`}>{category.name}</Link>
								</li>))};
                        </ul>
                    </div>
                </li>
                <li className="mb-1">
                    <button className="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="false">Admins</button>
                    <div className="collapse" id="orders-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            <li><Link className="dropdown-item" to="/administrador">Crear admins</Link></li>
                        </ul>
                    </div>
                </li>
                <li className="border-top my-3"></li>
                <li className="mb-1">
                    <button className="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#account-collapse" aria-expanded="false">Account</button>
                    <div className="collapse" id="account-collapse">
                        <ul className="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                            
                        </ul>
                    </div>
                </li>
            </ul>
        </div>
    )
}