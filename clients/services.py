import csv
import click
import os
from clients.models import Client

class ClientService:
    def __init__(self, table_name):
        self.table_name = table_name

    def create_client(self, client):
        with open(self.table_name, mode="a") as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerow(client.to_dict())

    def list_client(self):
        try:
            with open(self.table_name, mode="r") as f:
                reader = csv.DictReader(f, fieldnames=Client.schema())
                return list(reader)
        except FileNotFoundError: 
            click.echo("No clients to list Pls create a client to init the db")
            return

    def update_client(self, updated_client):
        clients = self.list_client()
        updated_clients = []
        for client in clients:
            if client["uid"] == updated_client.uid:
                updated_clients.append(updated_client.to_dict())
            else:
                updated_clients.append(client)
        self._save(updated_clients)


    def client_delete(self, client_id):
        clients = self.list_client()
        updated_clients = []
        for client in clients:
            if client["uid"] != client_id:
                updated_clients.append(client)
            else:
                click.echo(f"{client['name']} Deleted")
        self._save(updated_clients)



    def _save(self, clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode="a") as f:
            writer = csv.DictWriter(f, fieldnames=Client.schema())
            writer.writerows(clients)

        # remove and update temporary css
        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
