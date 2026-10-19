# Personal Portfolio

## About

A responsive personal portfolio for Akash Mahesh, an Information Science and Engineering student at BMS College of Engineering interested in software development, AI, and cloud computing.

## Features

- Responsive single-page layout for desktop, tablet, and mobile
- Project cards for machine learning, network security, and full-stack development work
- Experience timeline, skills toolkit, education, and certification sections
- Smooth scrolling, scroll reveal animations, active navigation, mobile menu, and back-to-top control
- No build step or JavaScript dependencies

## Technologies

- HTML5
- CSS3
- Vanilla JavaScript
- Nginx and Docker

## Running Locally

Open `index.html` directly in a browser. No Node.js, npm, or other installation is required.

## Running with Docker

From this folder, build and run the Nginx container:

```powershell
docker build -t akash-portfolio .
docker run --name akash-portfolio-container -p 8080:80 akash-portfolio
```

Visit http://localhost:8080 in a browser. Stop and remove the container with:

```powershell
docker stop akash-portfolio-container
docker rm akash-portfolio-container
```

## Project Structure

```text
Exercise 0 - Portfolio Website/
|-- index.html
|-- style.css
|-- script.js
|-- Dockerfile
|-- README.md
`-- .gitignore
```

## DevOps

This static website is containerized using Docker and served using Nginx. The Dockerfile copies the site into the Nginx web root, exposes port 80, and allows the site to run consistently without a local Node.js environment.

### Beginner Docker Checklist

1. Check Docker: open PowerShell and run `docker --version`.
2. If it is not installed, download Docker Desktop for Windows from https://www.docker.com/products/docker-desktop/ and complete the installer. Restart Windows if the installer asks you to.
3. Open Docker Desktop, wait until it says Docker is running, then verify with `docker run hello-world`.
4. Build the image from this folder with `docker build -t akash-portfolio .`.
5. Run it with `docker run --name akash-portfolio-container -p 8080:80 akash-portfolio` and open http://localhost:8080.
6. Stop and remove it with `docker stop akash-portfolio-container` and `docker rm akash-portfolio-container`.

### GitHub

This portfolio is Exercise 0 in the DevOps submissions repository. From the repository root, stage and push it with the other lab work:

```powershell
git add -- "Exercise 0 - Portfolio Website"
git commit -m "Update Exercise 0 portfolio website"
git push
```
