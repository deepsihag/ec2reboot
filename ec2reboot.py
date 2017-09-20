import click
import boto3
from botocore.exceptions import ClientError

@click.command()
@click.option('--name', '-n', multiple=True, default='', help='value of name tag')
@click.option('--no-reboot', is_flag=True, default=False, help='prints list only, does not reboot')
@click.option('--reboot-all', is_flag=True, default=False,
              help='initiate reboot in a single request instead iterating through the list')
def cli(name, no_reboot, reboot_all):
    """Return a list of private IPs of EC2 instances with given
    name tag and then iterate through the list to reboot each instance."""
    names = []
    if no_reboot and reboot_all:
        click.echo("Error: --no-reboot and --reboot-all can not be used together")
        exit()
    for n in name:
        names.append('{0}'.format(n))
    if len(names) == 0:
        click.echo("No name tag provided")
    else:
        ec2 = boto3.client('ec2')
        instance_list = {}
        try:
            response = ec2.describe_instances(Filters=[{'Name': 'tag:Name',
                                                        'Values': names}],)['Reservations']
            click.echo("InstanceId \t\t PrivateIpAddress")
            for i in range(len(response)):
                instances = response[i]['Instances']
                for j in range(len(instances)):
                    click.echo(instances[j]['InstanceId']+" \t "+instances[j]['PrivateIpAddress'])
                    instance_list[instances[j]['InstanceId']] = instances[j]['PrivateIpAddress']
            if not no_reboot:
                resp = yes_or_no("Initiate reboot")
                if resp:
                    if reboot_all:
                        click.echo("Rebooting all listed instances")
                        ec2.reboot_instances(InstanceIds=instance_list.keys())
                    else:
                        for key, value in instance_list.items():
                            click.echo("Rebooting instance %s with IP %s" % (key, value))
                            ec2.reboot_instances(InstanceIds=[key])
        except ClientError as e:
            print('Error', e)

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("please enter (y/n):")
