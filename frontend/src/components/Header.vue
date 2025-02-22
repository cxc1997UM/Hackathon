<template>
  <header class="header">
    <div class="logo">
      iGrade<span class="dot-ai">.ai</span>
    </div>
    <nav>
      <ul>
        <li><a href="#">Home</a></li>
        <li><a href="#">About</a></li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: "Header",
};
</script>

<style>
/* Header styling */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--secondary-color); /* White */
  color: var(--text-color);                /* Dark text */
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

/* Pastel blue for the ".ai" part */
.dot-ai {
  color: var(--primary-color);
}

/* Simple nav styling */
nav ul {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding: 0;
}

nav a {
  text-decoration: none;
  color: var(--text-color);
  font-weight: 500;
}

nav a:hover {
  color: var(--accent-color); /* Red on hover */
}
</style>
