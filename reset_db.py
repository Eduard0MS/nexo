import os
import django
import dotenv

# Carregar variáveis de ambiente do arquivo .env
dotenv.load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nexus.settings")
django.setup()

from django.db import transaction
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

print("Iniciando limpeza completa do banco de dados de autenticação social...")

try:
    # Usar transação para garantir que tudo seja feito ou nada
    with transaction.atomic():
        # 1. Remover todas as contas sociais e tokens (se existirem)
        social_accounts_count = SocialAccount.objects.all().count()
        SocialAccount.objects.all().delete()
        print(f"Removidas {social_accounts_count} contas sociais")

        social_tokens_count = SocialToken.objects.all().count()
        SocialToken.objects.all().delete()
        print(f"Removidos {social_tokens_count} tokens sociais")

        # 2. Remover todos os aplicativos sociais
        apps_count = SocialApp.objects.all().count()
        SocialApp.objects.all().delete()
        print(f"Removidos {apps_count} aplicativos sociais")

        # 3. Configurar o site
        site = Site.objects.get(id=1)
        old_domain = site.domain
        site.domain = "127.0.0.1:8000"
        site.name = "Nexo Local"
        site.save()
        print(f"Site atualizado: {old_domain} -> {site.domain}")

        # 4. Criar novo aplicativo Google
        google_app = SocialApp.objects.create(
            provider="google",
            name="Google OAuth",
            client_id=os.environ.get("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID_HERE"),
            secret=os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_CLIENT_SECRET_HERE"),
            key="",
        )
        print(f"Criado novo aplicativo Google com ID: {google_app.id}")

        # 5. Associar aplicativo ao site
        google_app.sites.add(site)
        print(f"Aplicativo associado ao site {site.domain}")

    print("Transação concluída com sucesso!")

except Exception as e:
    print(f"ERRO: {e}")

# Verificação final
print("\nVerificando resultado:")
print(f"Aplicativos sociais: {SocialApp.objects.count()}")
for app in SocialApp.objects.all():
    print(f"  ID: {app.id}, Provider: {app.provider}, Nome: {app.name}")
    print(f"  Sites associados: {', '.join([s.domain for s in app.sites.all()])}")

print("\nReinicie o servidor Django para aplicar as alterações!")
