resource "aws_security_group" "https_inbound_and_outbound_security_group" {
  # TODO - Configure the VPC ID when decided.
  # vpc_id = ""

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict CIDR range here.
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict CIDR range here.
  }

  tags = {
    Name = "Inbound and Outbound HTTPS - Managed by Terraform"
  }
}

resource "aws_security_group" "outbound_postgresql_security_group" {
  # TODO - Configure the VPC ID when decided.
  # vpc_id = ""

  tags = {
    Name = "Outbound PostgreSQL - Managed by Terraform"
  }
}

resource "aws_vpc_security_group_egress_rule" "outbound_postgres_rule" {
  security_group_id = aws_security_group.outbound_postgresql_security_group.id
  ip_protocol       = "tcp"
  from_port         = 5432
  to_port           = 5432

  referenced_security_group_id = aws_security_group.inbound_postgres_security_group.id

  tags = {
    Name = "Outbound PostgreSQL Rule - Managed by Terraform"
  }
}

resource "aws_security_group" "inbound_postgres_security_group" {
  # TODO - Configure the VPC ID when decided.
  # vpc_id = ""

  tags = {
    Name = "Inbound PostgreSQL - Managed by Terraform"
  }
}

resource "aws_vpc_security_group_ingress_rule" "inbound_postgres_rule" {
  security_group_id = aws_security_group.inbound_postgres_security_group.id
  ip_protocol       = "tcp"
  from_port         = 5432
  to_port           = 5432

  referenced_security_group_id = aws_security_group.outbound_postgresql_security_group.id

  tags = {
    Name = "Inbound PostgreSQL Rule - Managed by Terraform"
  }
}