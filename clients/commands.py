import click 
from clients.services import ClientService
from clients.models import Client

@click.group()
def clients():
    """Manage the clients lifecycle"""
    pass


@clients.command()
@click.option('-n', '--name', type=str, prompt=True, help="The client name")
@click.option('-c', '--company', type=str, prompt=True, help="The client company")
@click.option('-p', '--position', type=str, prompt=True, help="The client position")
@click.option('-e', '--email', type=str, prompt=True, help="The client email")
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new client"""
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj["clients_table"])

    client_service.create_client(client)


@clients.command()
@click.pass_context
def list(ctx):
    """ List all clients"""
    client_service = ClientService(ctx.obj["clients_table"])
    client_list = client_service.list_client()
    click.echo(f"ID  |  NAME  | COMPANY  |  EMAIL  |  POSITION")
    click.echo("*"*50)
    try:
        for client in client_list:
            click.echo(f"{client['uid']}  | {client['name']}  |  {client['company']}  |  {client['email']}  |  {client['position']}")
    except TypeError:
        click.echo("Clients Empty")


@clients.command()
@click.pass_context
@click.argument("client_uid")
def update(ctx, client_uid):
    """ Updates a client """
    client_service = ClientService(ctx.obj["clients_table"])

    client_list = client_service.list_client()
    client = [client for client in client_list if client["uid"] == client_uid]
    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)
        click.echo("Client update")
    else:
        click.echo("Client not found")

def _update_client_flow(client):
    click.echo("Leave empty if you dont wanna modify de value")
    client.name = click.prompt("New Name", type=str, default=client.name)
    client.company = click.prompt("New company", type=str, default=client.company)
    client.email = click.prompt("New email", type=str, default=client.email)
    client.position = click.prompt("New Position", type=str, default=client.position)
    return client


@clients.command()
@click.pass_context
def delete(ctx):
    """ Deleltes a client """
    client_id = click.prompt("Client ID to delete")
    client_service = ClientService(ctx.obj["clients_table"])
    client_service.client_delete(client_id)




all = clients

