# Contract Analyzer

Sistema de análise automática de contratos PDF usando FastAPI e processamento de linguagem natural.

## 🚀 Funcionalidades

- Upload de arquivos PDF via interface web
- Extração de texto usando OCR/parsing
- Análise de conteúdo com regex e IA
- Extração de informações contratuais importantes
- Geração de JSON estruturado
- Interface responsiva e amigável

## 🛠️ Tecnologias Utilizadas

- **Backend:**
  - Python 3.8+
  - FastAPI
  - PyPDF2
  - pdfplumber
  - OpenAI API (opcional)

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (Vanilla)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [url-do-repositorio]
cd contract-analyzer
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua-chave-api-aqui
```

## 🚀 Executando o projeto

1. Inicie o servidor backend:
```bash
cd src/backend
uvicorn main:app --reload
```

2. Abra o frontend:
Abra o arquivo `src/frontend/index.html` em seu navegador

## 📦 Estrutura do Projeto

```
contract-analyzer/
├── src/
│   ├── backend/
│   │   ├── core/
│   │   ├── modules/
│   │   └── shared/
│   └── frontend/
├── tests/
├── docs/
└── requirements.txt
```

## 📄 API Endpoints

- `POST /api/v1/contracts/analyze`
  - Aceita: arquivo PDF
  - Retorna: JSON com análise do contrato

## 🧪 Testes

Execute os testes com:
```bash
pytest
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✨ Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request