# Project Overview

This repository contains both client and server codebases for a fictional service based on the "Game of Thrones" series. The server provides access to a list of laws via a FastAPI endpoint, while the client is a Next.js application that interacts with this service.

## Server Setup

The server is implemented using FastAPI and runs inside a Docker container. It provides an API to query laws from the "Game of Thrones" universe.

### Prerequisites

- Docker installed on your machine
- An OpenAI API key (set in the `.env` file)

### Running the Server

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/silvisece/norm-ai-takehome-fullstack.git
   cd your-repo
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Build and Run the Docker Container**:
   ```bash
   docker build -t got-laws-api .
   docker run -d -p 80:80 --env-file .env got-laws-api
   ```

4. **Access the API**:
   - The API will be accessible at `http://localhost:80/query`.

## Client Setup

The client is a Next.js application that provides a minimal interface to interact with the server.

### Prerequisites

- Node.js and pnpm installed on your machine

### Running the Client

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   pnpm install
   ```

3. **Run the Development Server**:
   ```bash
   pnpm dev
   ```

4. **Access the Client**:
   - Open your browser and go to `http://localhost:3000` to interact with the application.

## Additional Information

- Ensure that both the server and client are running simultaneously to allow the client to communicate with the server.
- For any issues or questions, please refer to the respective README files in the `app` and `frontend` directories.


## Finally - Thoughts on the 2nd part of the assigment

What unique challenges do you foresee in developing and integrating AI regulatory agents for legal compliance from a full-stack perspective? How would you address these challenges to make the system robust [r] and user-friendly [u] ?

---

As Norm's AI regulatory agents scale across domains, they introduce new challenges in coordination, precision, cost, and adaptability. The challenges I exlore span agent conflicts, higher false positives/negatives, rising costs, and brittle logic structures. For each, I propose robust [r] and user-friendly [u] solutions to ensure Norm remains scalable, trustworthy, and adaptable to client needs.

---

#### 1. **Coordination Across Agents**
In a future where hundreds of AI regulatory agents are operating concurrently, disputes and inconsistencies will inevitably arise.

**Solution:**  
[r][u] Orchestrate agents using a centralized policy framework to ensure visibility and predictability. This builds user trust and grants Norm control over decision chains.

---

#### 2. **Handling Expanding Domain Scope**
As Norm scales into more complex and niche regulatory areas, the system will surface more issues—leading to higher false negatives and false positives. This can strain client teams and reduce confidence.

**Solutions:**  
[r] Continuously source high-quality, domain-specific legal data.  
[r][u] Offer confidence scores and evaluation metrics to guide decision-making without overwhelming users.  
[r][u] Design UI-integrated “escape hatches” for agent-human handoffs, enabling real-time intervention and correction.

---

#### 3. **Cost and Scalability Pressures**
Sophisticated reasoning increases compute costs. Additionally, internal client data volume will rise as adoption deepens.

**Solutions:**  
[r] Build triage systems to delegate simpler tasks to lightweight or cheaper models. (Maintenance of this layer may be challenging.)  
[r] Optimize model usage by smart routing, leveraging open-source models and traditional ML methods where appropriate.

---

#### 4. **Ontology and Personalization Strain**
As Norm expands across compliance domains, rigid ontologies or logic trees may become brittle—especially when clients request customization.

**Solutions:**  
[r][u] Strike the right balance between abstraction and client-specific input.  
[r][u] Allow for client-side overrides and systematically learn from them to evolve system intelligence.

---

#### 5. **Regulatory Drift and Client Responsiveness**
Ongoing regulation changes—and variance in client reactions—pose challenges for timely and accurate system updates.

**Solutions:**  
[r][u] Build configurable parameters and UI components that alert users to regulation changes and let them preview, accept, or postpone updates.