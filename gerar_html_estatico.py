import json

# Ler o JSON
with open('municipios_regioes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Criar arquivo HTML com dados incorporados
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta Região de Saúde - Ministério da Saúde</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0066cc 0%, #004d99 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 700px;
            width: 100%;
        }}

        h1 {{
            color: #134074;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}

        .search-box {{
            position: relative;
            margin-bottom: 20px;
        }}

        label {{
            display: block;
            margin-bottom: 8px;
            color: #134074;
            font-weight: 600;
        }}

        input[type="text"] {{
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            outline: none;
            transition: all 0.3s;
        }}

        input[type="text"]:focus {{
            border-color: #0066cc;
            box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
        }}

        button {{
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #0066cc 0%, #004d99 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 10px;
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 102, 204, 0.4);
        }}

        button:active {{
            transform: translateY(0);
        }}

        .result {{
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            display: none;
            animation: fadeIn 0.5s;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .result.success {{
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }}

        .result.error {{
            background: #ffebee;
            border-left: 4px solid #f44336;
        }}

        .result h3 {{
            color: #134074;
            margin-bottom: 15px;
            font-size: 20px;
        }}

        .result p {{
            color: #555;
            margin: 10px 0;
            line-height: 1.8;
            font-size: 15px;
        }}

        .result strong {{
            color: #134074;
        }}

        .suggestions {{
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 5px;
            display: none;
            background: white;
            position: absolute;
            width: 100%;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}

        .suggestion-item {{
            padding: 12px 18px;
            cursor: pointer;
            transition: background 0.2s;
            border-bottom: 1px solid #f5f5f5;
        }}

        .suggestion-item:last-child {{
            border-bottom: none;
        }}

        .suggestion-item:hover {{
            background: #f0f7ff;
        }}

        .suggestion-item .municipio-nome {{
            font-weight: 600;
            color: #134074;
        }}

        .suggestion-item .uf-tag {{
            display: inline-block;
            background: #0066cc;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-left: 8px;
        }}

        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }}

        .info-box {{
            background: #f0f7ff;
            border-left: 4px solid #0066cc;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .info-box p {{
            color: #134074;
            font-size: 14px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Consulta Região de Saúde</h1>
        <p class="subtitle">Ministério da Saúde - Secretaria de Atenção Primária à Saúde</p>
        
        <div class="info-box">
            <p>📍 Digite o nome do município para descobrir sua região de saúde</p>
        </div>

        <div class="search-box">
            <label for="municipio">Nome do Município:</label>
            <input type="text" id="municipio" placeholder="Ex: São Paulo, Rio de Janeiro, Brasília..." autocomplete="off">
            <div class="suggestions" id="suggestions"></div>
        </div>

        <button onclick="buscarRegiao()">🔍 Buscar Região de Saúde</button>

        <div class="result" id="result"></div>

        <div class="footer">
            <p>Dados atualizados em Outubro de 2025 | Ministério da Saúde</p>
        </div>
    </div>

    <script>
        // Dados incorporados diretamente no HTML
        const municipiosData = {json.dumps(data, ensure_ascii=False)};

        console.log('Total de municípios carregados:', municipiosData.length);

        // Autocomplete
        document.getElementById('municipio').addEventListener('input', function() {{
            const input = this.value.trim().toUpperCase();
            const suggestionsDiv = document.getElementById('suggestions');
            
            if (input.length < 2) {{
                suggestionsDiv.style.display = 'none';
                return;
            }}

            const matches = municipiosData.filter(m => 
                m.NO_MUNICIPIO.includes(input)
            ).slice(0, 10);

            if (matches.length > 0) {{
                suggestionsDiv.innerHTML = matches.map(m => 
                    `<div class="suggestion-item" onclick="selecionarMunicipio('${{m.NO_MUNICIPIO}}')">
                        <span class="municipio-nome">${{m.NO_MUNICIPIO}}</span>
                        <span class="uf-tag">${{m.UF}}</span>
                    </div>`
                ).join('');
                suggestionsDiv.style.display = 'block';
            }} else {{
                suggestionsDiv.style.display = 'none';
            }}
        }});

        function selecionarMunicipio(nome) {{
            document.getElementById('municipio').value = nome;
            document.getElementById('suggestions').style.display = 'none';
            buscarRegiao();
        }}

        // Fechar suggestions ao clicar fora
        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.search-box')) {{
                document.getElementById('suggestions').style.display = 'none';
            }}
        }});

        // Buscar região ao pressionar Enter
        document.getElementById('municipio').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                buscarRegiao();
            }}
        }});

        function buscarRegiao() {{
            const input = document.getElementById('municipio').value.trim().toUpperCase();
            const resultDiv = document.getElementById('result');
            
            if (!input) {{
                alert('Por favor, digite o nome do município');
                return;
            }}

            document.getElementById('suggestions').style.display = 'none';

            const encontrados = municipiosData.filter(m => m.NO_MUNICIPIO === input);

            if (encontrados.length === 0) {{
                resultDiv.className = 'result error';
                resultDiv.innerHTML = `
                    <h3>❌ Município não encontrado</h3>
                    <p>O município "<strong>${{input}}</strong>" não foi encontrado na base de dados.</p>
                    <p>Verifique a grafia e tente novamente.</p>
                `;
                resultDiv.style.display = 'block';
                return;
            }}

            // Agrupar por região de saúde (caso haja mais de uma)
            const regioes = [...new Set(encontrados.map(e => e.NO_REGIAO_SAUDE))];
            const uf = encontrados[0].UF;

            let html = `
                <h3>✅ Resultado da Consulta</h3>
                <p><strong>Município:</strong> ${{input}}</p>
                <p><strong>UF:</strong> ${{uf}}</p>
            `;

            if (regioes.length === 1) {{
                html += `<p><strong>Região de Saúde:</strong> ${{regioes[0]}}</p>`;
            }} else {{
                html += `<p><strong>Regiões de Saúde:</strong></p><ul>`;
                regioes.forEach(r => {{
                    html += `<li>${{r}}</li>`;
                }});
                html += `</ul>`;
            }}

            resultDiv.className = 'result success';
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
        }}
    </script>
</body>
</html>"""

# Salvar o arquivo
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Arquivo index.html criado com sucesso!')
print(f'Total de municípios incorporados: {len(data)}')
print('Agora você pode abrir o arquivo index.html diretamente no navegador.')
