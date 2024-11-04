import asyncio
import zipfile
import os
from playwright.async_api import Playwright, async_playwright

async def run(playwright: Playwright, ano_mes: str, timeout: int, download_path: str, download_zipfile: str, extract_path: str) -> None:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"

    try:
        browser = await playwright.firefox.launch(
                    headless=True,
                    args=['--no-sandbox'], timeout=timeout
                )  
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        # Vai para a página de download
        await page.goto("https://consumidor.gov.br/pages/dadosabertos/externo/", wait_until="domcontentloaded")
        await page.locator("[name='publicacoesDT_length']").select_option("25", timeout=timeout)
        
        # Garante que o diretório de download e extração exista
        os.makedirs(download_path, exist_ok=True)
        os.makedirs(extract_path, exist_ok=True)
            
        async with page.expect_download(timeout=timeout) as download_info:
            async with page.expect_popup(timeout=timeout) as page1_info:
                # Passa o valor do ano_mes para o seletor de download correto
                await page.get_by_title(f"Download 'finalizadas_{ano_mes}.zip' ").click(timeout=timeout)
            page1 = await page1_info.value

        # Captura o download e salva o arquivo .zip no local especificado
        download = await download_info.value
        await download.save_as(download_zipfile)  # Salva o arquivo .zip no caminho especificado

        # Fecha o popup
        await page1.close()

        # Fecha o navegador
        await context.close()
        await browser.close()

        # Descompactar o arquivo .zip
        with zipfile.ZipFile(download_zipfile, 'r') as zip_ref:
            zip_ref.extractall(extract_path)  # Extrai todos os arquivos para a pasta de destino
        
        print(f"Arquivo descompactado com sucesso em: {extract_path}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

async def main() -> None:
    # Defina os parâmetros aqui
    ano_mes = os.getenv("ANO_MES", "2024-05")  # Parâmetro ano-mês
    timeout = int(os.getenv("TIMEOUT", 600000))  # Timeout em milissegundos
    download_path = os.getenv("DOWNLOAD_PATH", "downloads")  # Caminho de download
    download_zipfile = os.path.join(download_path, f"finalizadas_{ano_mes}.zip")  # Nome do arquivo .zip
    extract_path = os.getenv("EXTRACT_PATH", "dados")  # Pasta de extração

    async with async_playwright() as playwright:
        await run(playwright, ano_mes, timeout, download_path, download_zipfile, extract_path)

if __name__ == "__main__":
    asyncio.run(main())
