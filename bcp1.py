import hashlib
import json
import time
from uuid import uuid4
import tkinter as tk
from tkinter import messagebox

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_block(nonce=1, previous_hash='0')

    def create_block(self, nonce, previous_hash):
        block = Block(len(self.chain), self.pending_transactions, previous_hash, nonce)
        self.chain.append(block)
        self.pending_transactions = []
        return block

    def add_transaction(self, sender, recipient, amount, contract=None):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'contract': contract
        }
        self.pending_transactions.append(transaction)
        return self.last_block.index + 1

    def execute_smart_contracts(self):
        for tx in self.pending_transactions:
            if tx['contract']:
                condition = tx['contract'].get('condition')
                action = tx['contract'].get('action')
                if eval(condition):  # Simple execution (unsafe for real-world use!)
                    tx['recipient'] = action['recipient']
                    tx['amount'] = action['amount']
                    print(f"Contract Executed: {tx}")

    def proof_of_work(self, difficulty=4):
        nonce = 0
        while True:
            block = Block(len(self.chain), self.pending_transactions, self.last_block.hash, nonce)
            if block.hash[:difficulty] == '0' * difficulty:
                return nonce
            nonce += 1

    def mine_block(self):
        self.execute_smart_contracts()
        nonce = self.proof_of_work()
        previous_hash = self.last_block.hash
        return self.create_block(nonce, previous_hash)

    @property
    def last_block(self):
        return self.chain[-1]

class BlockchainUI:
    def __init__(self, root):
        self.blockchain = Blockchain()
        self.root = root
        self.root.title("Blockchain UI")
        
        self.sender_label = tk.Label(root, text="Sender:")
        self.sender_label.pack()
        self.sender_entry = tk.Entry(root)
        self.sender_entry.pack()
        
        self.recipient_label = tk.Label(root, text="Recipient:")
        self.recipient_label.pack()
        self.recipient_entry = tk.Entry(root)
        self.recipient_entry.pack()
        
        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()
        
        self.add_transaction_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.pack()
        
        self.mine_button = tk.Button(root, text="Mine Block", command=self.mine_block)
        self.mine_button.pack()
        
        self.chain_button = tk.Button(root, text="Show Blockchain", command=self.show_chain)
        self.chain_button.pack()
    
    def add_transaction(self):
        sender = self.sender_entry.get()
        recipient = self.recipient_entry.get()
        amount = self.amount_entry.get()
        if sender and recipient and amount.isdigit():
            self.blockchain.add_transaction(sender, recipient, int(amount))
            messagebox.showinfo("Success", "Transaction Added!")
        else:
            messagebox.showerror("Error", "Invalid Transaction Details")
    
    def mine_block(self):
        self.blockchain.mine_block()
        messagebox.showinfo("Success", "Block Mined!")
    
    def show_chain(self):
        chain_str = json.dumps([block.__dict__ for block in self.blockchain.chain], indent=4)
        messagebox.showinfo("Blockchain", chain_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainUI(root)
    root.mainloop()
