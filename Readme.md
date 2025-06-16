<h1 align="center" id="title">Flask Marketplace Backend API</h1>

<p align="center"><img src="https://socialify.git.ci/Yuriamani/Nairobi-Konnekt-Marketplace-backend-/image?language=1&amp;owner=1&amp;name=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p id="description">A RESTful API backend for an e-commerce marketplace built with Flask SQLAlchemy and PostgreSQL.</p>

<p align="center"><img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="shields"><img src="https://img.shields.io/badge/Flask-2.0+-green.svg" alt="shields"><img src="https://img.shields.io/badge/PostgreSQL-13+-blue.svg" alt="shields"></p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Product management (CRUD operations)
*   Vendor management
*   Product categorization
*   Featured new arrivals and best-seller sections
*   Pagination with cursor-based navigation
*   Search functionality
*   Related products suggestions

## <h2>🔌 API Endpoints</h2>

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>/products</code></td>
    <td>GET</td>
    <td>Parameters: `limit` (Max items to return, default: 10, max: 50), `cursor` (Last seen ID for pagination), `category` (Filter by category), `section` (Filter by section: 'featured', 'new-arrivals', 'best-sellers'), `search` (Search term for product name/description). Returns paginated list of products.</td>
  </tr>
  <tr>
    <td><code>/products/{id}</code></td>
    <td>GET</td>
    <td>Get single product</td>
  </tr>
  <tr>
    <td><code>/products</code></td>
    <td>POST</td>
    <td>Required fields: name, price, vendor_id, category. Creates a new product.</td>
  </tr>
  <tr>
    <td><code>/products/{id}</code></td>
    <td>PATCH</td>
    <td>Updates product fields</td>
  </tr>
  <tr>
    <td><code>/products/{id}</code></td>
    <td>DELETE</td>
    <td>Deletes a product</td>
  </tr>
  <tr>
    <td><code>/categories</code></td>
    <td>GET</td>
    <td>Returns list of all unique product categories</td>
  </tr>
  <tr>
    <td><code>/products/overview</code></td>
    <td>GET</td>
    <td>Returns preview of featured, new arrivals, and best-seller products</td>
  </tr>
</table>

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository</p>

```
git clone git@github.com:Yuriamani/Nairobi-Konnekt-Marketplace-backend-.git
```

<p>2. Create and activate a virtual environment:</p>

```
pipenv shell
```

<p>3. Install dependencies:</p>

```
pipenv install -r requirements.txt
```

<p>4. Set up environment variables:</p>

```
DATABASE_URL=your-postgress-database
```

<p>5. Initialize the database:</p>

```
flask db init  
```

```
flask db migrate
```

<p>7. Running the Application</p>

```
flask run
```

<h2>🍰 Contribution Guidelines:</h2>

1.Fork the repository 
2.Create a new branch for your feature 
3.Commit your changes 
4.Push to the branch 
5.Create a Pull Request

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python 3.8+
*   PostgreSQL
*   pip/pipenv

<h2>🛡️ License:</h2>

<p>This project is licensed under the <a href="LICENSE">MIT License</a>.</p>

<h2>💖Like my work?</h2>