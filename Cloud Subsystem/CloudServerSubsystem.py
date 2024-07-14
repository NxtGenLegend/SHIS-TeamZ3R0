from cgi import test
import os
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
z3r0server = boto3.resource('ec2')

def KeyPairFunction(accesskey, privatekeyfile=None):
    
    try:
        keypair = z3r0server.KeyPairFunction(keycode=accesskey)
        logger.info("The key has been created %s.", keypair.name)
        if privatekeyfile is not None:
            with open(privatekeyfile, 'w') as pk_file:
                pk_file.write(keypair.key_material)
            logger.info("Private key stored at %s.", privatekeyfile)
    except ClientError:
        logger.exception("The key could not be created %s.", accesskey)
        raise
    else:
        return keypair

def security(groupname, groupdesc, sship=None):
    try:
        dvpcs = list(z3r0server.vpcs.filter(
            Filters=[{'Name': 'isDefault', 'Values': ['true']}]))[0]
        logger.info("Using Default Virtual Private Cloud Server %s.", dvpcs.id)
    except ClientError:
        logger.exception("No Virtual Private Cloud Server Found")
        raise
    except IndexError:
        logger.exception("No Virtual Private Cloud Server On List")
        raise

    try:
        secgrping = dvpcs.create_security_group(
            GroupName=groupname, Description=groupdesc)
        logger.info(
            "Security Has Been Installed In This Virtual Private Cloud Server: %s.", groupname, dvpcs.id)
    except ClientError:
        logger.exception("Security Has Not Been Installed In This Virtual Private Server: %s.", groupname)
        raise

    try:
        ipperms = [{
            'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }, {
            'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
        if sship is not None:
            ipperms.append({
                'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22,
                'IpRanges': [{'CidrIp': f'{sship}/32'}]})
        secgrping.authorize_ingress(IpPermissions=ipperms)
        logger.info("Set inbound rules for %s to allow all inbound HTTP & HTTPS"
                    "but only %s for SSH", secgrping.id, sship)
    except ClientError:
        logger.exception("Cannot authorize inbound rules for %s", groupname)
        raise
    else:
        return secgrping
    
def awsec2instance(
        image, instancetype, accesskey, secgrpnames=None):
    try:
        instance_params = {
            'ImageId': image, 'InstanceType': instancetype, 'KeyName': accesskey
        }
        if secgrpnames is not None:
            instance_params['SecurityGroups'] = secgrpnames
        instance = z3r0server.create_instances(
            **instance_params, Min=1, Max=1)[0]
        logger.info("The instance has been created, with ID: %s.", instance.id)
    except ClientError:
        logging.exception(
            "The instance with image %s, instance type %s, and key %s has not been created",
            image, instancetype, accesskey)
        raise
    else:
        return instance



def delkeypair(accesskey, privatekeyfile):
    try:
        z3r0server.KeyPair(accesskey).delete()
        os.remove(privatekeyfile)
        logger.info("The key %s & private key file %s have been deleted",
                    accesskey, privatekeyfile)
    except ClientError:
        logger.exception("The key %s could not be deleted", accesskey)
        raise

def delsecgrp(secgrpid):
    try:
        z3r0server.SecurityGroup(secgrpid).delete()
        logger.info("The security group %s has been deleted", secgrpid)
    except ClientError:
        logger.exception("The security group %s could not be deleted", secgrpid)
        raise

def delinstance(instance_id):
    try:
        z3r0server.Instance(instance_id).terminate()
        logger.info("The instance %s has been deleted", instance_id)
    except ClientError:
        logging.exception("The instance %s could not be deleted", instance_id)
        raise
    
    

def startinstance(instance_id):
    try:
        instancestartvalue = z3r0server.Instance(instance_id).start()
        logger.info("The instance %s has been started", instance_id)
    except ClientError:
        logger.exception("The instance %s could not be started", instance_id)
        raise
    else:
        return instancestartvalue

def stopinstance(instance_id):

    try:
        response = z3r0server.Instance(instance_id).stop()
        logger.info("The instance %s has been stopped", instance_id)
    except ClientError:
        logger.exception("The instance %s could not be stopped", instance_id)
        raise
    else:
        return response
    

def output(instance_id):
    try:
        output = z3r0server.Instance(instance_id).console_output()['Output']
        logger.info("Output received for instance: %s", instance_id)
    except ClientError:
        logger.exception(
            ("Output not received for instance: %s", instance_id))
        raise
    else:
        return output
    

def changesecgrp(instance_id, secgrp_id, newsecgrp_id):
    try:
        for ni in z3r0server.Instance(instance_id).network_interfaces:
            group_ids = [group['GroupId']
                         for group in ni.groups]
            if secgrp_id in group_ids:
                try:
                    ni.modify_attribute(
                        Groups=[newsecgrp_id
                                if secgrp_id == group_id else group_id
                                for group_id in group_ids])
                    logger.info(
                        "Swapped %s with %s for %s", secgrp_id,
                        newsecgrp_id, ni.id)
                except ClientError:
                    logger.exception(
                        "Security groups for %s could not be updated", ni.id)
    except ClientError:
        logger.exception(
            "Could not get Network interfaces for %s", instance_id)
        raise
