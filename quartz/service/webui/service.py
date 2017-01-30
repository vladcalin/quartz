from gemstone import MicroService, public_method


class QuartzWebuiMicroservice(MicroService):
    name = "quartz.webui"


if __name__ == '__main__':
    cli = QuartzWebuiMicroservice().get_cli()
    cli()
