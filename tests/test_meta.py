from peak import Peak, name_outputs, rebind_type
from hwtypes import Bit, BitVector, SMTBit, SMTBitVector
from hwtypes.adt import Sum, Product
from examples.alu import gen_alu, Inst, ALUOP


def test_meta():
    x = 5
    stack = 4
    env = 3
    class A(Peak):
        def __init__(self):
            self.x = x
            self.stack = stack
    assert hasattr(A,"_env_")
    assert A._env_['x'] == 5
    assert A._env_['stack'] == 4
    assert A._env_['env'] == 3

    def f():
        x = 4
        stack = 2
        env = 1
        class A1(Peak):
            pass
        return A1
    A1 = f()
    assert hasattr(A1,"_env_")
    assert A1._env_['x'] == 4
    assert A1._env_['stack'] == 2
    assert A1._env_['env'] == 1


Data = BitVector[16]
#Bug in inspect.getsource if I try to name this class to A
BV = BitVector
DBSum = Sum[Data,BV[8]]
class Instr(Product):
    a=DBSum
    b=Bit

def test_rebind_type():
    Instr_smt = rebind_type(Instr,SMTBitVector.get_family())
    assert Instr_smt.a == Sum[SMTBitVector[16],SMTBitVector[8]]
    assert Instr_smt.b == SMTBit

def test_rebind():
    class B(Peak):
        def __init__(self):
            self.Data = Data
        @name_outputs(out=BV[16])
        def __call__(self, instr : Instr, a : Data):
            return a + BitVector[16](5)

    assert Data(6) == B()(None,Data(1))
    B_smt = B.rebind(SMTBitVector.get_family())
    assert B_smt().Data == SMTBitVector[16]
    Instr_smt = rebind_type(Instr,SMTBitVector.get_family())
    instr_smt = Instr_smt(a=Instr_smt.a(SMTBitVector[8](9)),b=SMTBit(0))
    assert SMTBitVector[16](10) == B_smt()(instr=instr_smt,a=SMTBitVector[16](5))


ALU = gen_alu(BitVector.get_family())
def test_alu():
    assert hasattr(ALU,"_env_")
    Data = BitVector[16]
    assert ALU()(Inst(ALUOP.Add),Data(3),Data(5)) == Data(8)
    ALU_smt = ALU.rebind(SMTBitVector.get_family())
    alu_smt = ALU_smt()
    Data = SMTBitVector[16]
    assert alu_smt(Inst(ALUOP.Add),Data(3),Data(5)) == Data(8)
    #Try to pass in original bitvector to smt
    Data = BitVector[16]
    try:
        alu_smt(Inst(ALUOP.Add),Data(3),Data(5))
    except TypeError:
        pass
    else:
        assert 0
