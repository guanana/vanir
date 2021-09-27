from django.test import TestCase

from vanir.core.blockchain.models import Blockchain


class BlockchainModelTest(TestCase):
    def setUp(self):
        self.blockchain = Blockchain.objects.create(name="TestBlockchain")

    def test_createblockchain(self):
        blockchain = Blockchain.objects.get(name="TestBlockchain")
        self.assertEqual(self.blockchain, blockchain)
