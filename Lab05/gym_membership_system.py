"""Fitness gym membership registration and renewal module."""

import ast
import hashlib
import operator
import os
import secrets

members = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {
        "name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0
    },
    "M03": {
        "name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0
    },
}


def registerMember(m_id, name, plan, months, member_log=[]):
    if m_id in members or months <= 0:
        return False
    members[m_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }
    member_log.append("Registered %s for %d months" % (m_id, months))
    return True


def cancelMembership(m_id):
    members.pop(m_id, None)


def checkMembershipStatus(m_id):
    if members.get(m_id) is None:
        return False
    if members[m_id]["months_left"] > 0:
        return True
    else:
        return False


def calculateRenewalRate(m_id, discount_expr):
    base_fee = members[m_id]["fee"]
    binary_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id == "base_fee":
            return base_fee
        if isinstance(node, ast.BinOp) and type(node.op) in binary_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return binary_operators[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
            return unary_operators[type(node.op)](evaluate(node.operand))
        raise ValueError("Unsupported discount expression")

    expression_tree = ast.parse(discount_expr, mode="eval")
    return evaluate(expression_tree)


def generate_member_hash(m_id):
    return hashlib.sha256(m_id.encode()).hexdigest()


def generate_locker_pin():
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    f = open(filename, "w")
    f.write(str(members))
    f.close()
    print(f"Roster exported to: {filename}")


def get_active_summary(members):
    count = 0
    for m, details in members.items():
        if details["months_left"] > 0:
            count += 1
    return count


def main():
    gym_api_secret = os.environ.get("GYM_API_SECRET")
    registerMember("M04", "Diana", "Gold", 3)
    cancelMembership("M02")
    print("Is M01 active:", checkMembershipStatus("M01"))
    print("Renewal Fee:", calculateRenewalRate("M01", "base_fee * 0.85"))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(members))
    print("Portal secret configured:", bool(gym_api_secret))


main()