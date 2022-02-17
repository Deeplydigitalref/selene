from pyfuncify import monad

from .. model import base_model
from common import error

def find_or_create_circuit(domain) -> base_model.Circuit:
    circuit = find_circuit_by_id(domain.circuit_name)
    if circuit.is_left():
        return create_circuit(domain.circuit_name)
    return circuit.value

def create_circuit(circuit_name) -> base_model.Circuit:
    repo = base_model.Circuit(hash_key=format_circuit_pk(circuit_name),
                              range_key=format_circuit_sk(circuit_name),
                              circuit_state=None,
                              last_state_chg_time=None,
                              failures=0)
    repo.save()
    return repo

def update_circuit(domain, repo: base_model.Circuit) -> base_model.Circuit:
    repo.failures = domain.failures
    repo.last_state_chg_time = domain.last_state_chg_time
    repo.circuit_state = domain.circuit_state
    repo.save()
    return repo

@monad.monadic_try("find_circuit_by_id", error_cls=error.DynamoError)
def find_circuit_by_id(id):
    return base_model.Circuit.get(format_circuit_pk(id), format_circuit_sk(id))

@monad.monadic_try("all_circuits", error_cls=error.DynamoError)
def all_circuits(ids):
    keys = [(format_circuit_pk(id), format_circuit_sk(id)) for id in ids]
    return base_model.Circuit.batch_get(keys)


def format_circuit_pk(name):
    return ("CIR#" + "{}").format(name)

def format_circuit_sk(name):
    return ("CIR#" + "{}").format(name)
