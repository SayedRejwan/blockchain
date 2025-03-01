import hashlib
import json
import time
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

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
        self.root.title("Blockchain Wallet")
        self.root.geometry("400x600")
        self.root.configure(bg='#1B1B2F')

        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Arial", 12), background='#162447', foreground='white')
        self.style.configure("TLabel", font=("Arial", 12), background='#1B1B2F', foreground='white')
        
        ttk.Label(root, text="Available Balance:").pack(pady=5)
        self.balance_label = ttk.Label(root, text="$ 18,420.81", font=("Arial", 16, "bold"))
        self.balance_label.pack(pady=5)
        
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        self.pay_button = ttk.Button(frame, text="Pay", command=self.add_transaction)
        self.pay_button.grid(row=0, column=0, padx=10)

        self.request_button = ttk.Button(frame, text="Request", command=self.mine_block)
        self.request_button.grid(row=0, column=1, padx=10)

        ttk.Label(root, text="My Transactions:").pack(pady=5)
        self.tree = ttk.Treeview(root, columns=("Type", "Amount", "Status"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Status", text="Status")
        self.tree.pack(pady=10)

    def add_transaction(self):
        self.blockchain.add_transaction("User", "Recipient", 50)
        self.update_transactions()
        messagebox.showinfo("Success", "Transaction Added!")

    def mine_block(self):
        self.blockchain.mine_block()
        self.update_transactions()
        messagebox.showinfo("Success", "Block Mined!")

    def update_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for tx in self.blockchain.pending_transactions:
            self.tree.insert("", "end", values=(tx['sender'], tx['amount'], "Pending"))
        for block in self.blockchain.chain:
            for tx in block.transactions:
                self.tree.insert("", "end", values=(tx['sender'], tx['amount'], "Confirmed"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainUI(root)
    root.mainloop()
