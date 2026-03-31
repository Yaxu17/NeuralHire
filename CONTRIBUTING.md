# Contributing to NeuralHire

Thanks for your interest in contributing! Here's how to get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/your-username/neuralhire.git
cd neuralhire
```
3. Follow the setup guide in [SETUP.md](SETUP.md)
4. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

## Making Changes

- Keep code clean and well-commented
- Follow existing code style (PEP8 for Python)
- Test your changes before submitting

## Running Tests

```bash
cd backend
venv\Scripts\activate
pytest tests/ -v
```

## Submitting a Pull Request

1. Push your branch: `git push origin feature/your-feature-name`
2. Open a Pull Request on GitHub
3. Describe what you changed and why

## Ideas for Contributions

- Add more embedding model options
- Build a login/auth system
- Add export to CSV feature
- Improve match summary generation
- Add bulk resume upload
- Write more tests
