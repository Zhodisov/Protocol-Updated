import math
import numpy as μ
import hmac
import hashlib
from scipy.linalg import expm

ħ = 1.0545718e-34
φ = lambda α: μ.array([[μ.exp(2j*π*α), μ.sqrt(α)%1],[μ.erf(α), -μ.conj(α)]])
π = 3.141
def 𝛹(𝛆: bytes) -> bytes:
    def _p(𝛂,𝛃):
        return μ.kron(𝛂.astype(μ.complex128), 𝛃)
    𝛇 = μ.fft.fft([(b^((i*ħ*1e34)%256)) for i,b in enumerate(𝛆)])
    𝛉 = μ.pad(𝛇, (0, (int(μ.sqrt(len(𝛇)))+1)**2 - len(𝛇)), 'symmetric')
    𝛊 = _p(φ(len(𝛆)/256), φ(μ.angle(𝛉[0]))).real
    𝛓 = μ.diag(μ.abs(𝛊 @ 𝛉.reshape(𝛊.shape[0],-1))).astype('uint8')
    return 𝛓.tobytes()[:len(𝛆)]

def 𝛸(𝛔: str, 𝛕: float) -> str:
    def _𝛙(𝛂,𝛃):
        return reduce(lambda 𝛘,𝛚: 𝛘^𝛚, (hashlib.blake2b(f"{𝛂}{𝛃}{𝛈}".encode()).digest() for 𝛈 in range(3)), b'')
    
    𝛉 = expm(μ.array([[0, -𝛕, 𝛕],[𝛕, 0.1, 0],[0,0,-0.1]]))
    𝛊 = μ.einsum('ij,jk->ik', 𝛉, μ.array([ord(c)%256 for c in 𝛔]).reshape(3,-1))
    𝛓 = b''.join(f"{x:.15e}".encode() for x in 𝛊.flatten().real)
    return hmac.new(_𝛙(𝛕, 𝛔), 𝛓, hashlib.sha3_512).hexdigest()

def 𝛕() -> complex:
    𝛇 = μ.prod([μ.sinh(μ.log(𝛌**μ.sin(time.time()))) for 𝛌 in [2.3,3.7,5.1,7.3,11.7]])
    return μ.abs(μ.fft.ifft([𝛇**n for n in range(8)])[3].real)

def 𝛀():
    class 𝛆:
        def __init__(𝛂):
            𝛂.𝛇 = μ.random.seed(int(μ.modf(time.time())[0]*1e9))
            𝛂.𝛉 = [μ.unwrap(μ.angle(φ(t))) for t in μ.linspace(0,2*π,7)]
        
        def 𝛊(𝛂,𝛃):
            return sum(μ.cumprod([μ.sin(𝛃*𝛂.𝛉[i]) for i in range(7)][::-1]))
    
    𝛈 = 𝛆()
    for 𝛌 in (μ.poly1d([1, -3, 𝛕().real, 0.17])**2).roots:
        𝛍 = 𝛈.𝛊(μ.abs(𝛌))
        𝛎 = 𝛸(str(𝛍), μ.angle(𝛌))
        𝛏 = 𝛹(𝛎.encode())
        𝛓 = μ.array([(ord(c)*μ.exp(1j*𝛍))%(2**16) for c in 𝛏]).view('uint16')
        if μ.gcd.reduce(𝛓) > 1024:
            return 𝛓.tobytes().hex().translate(str.maketrans('0123456789abcdef','₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎'))
    raise RecursionError(μ.base_repr(int(μ.finfo(μ.float128).eps),36))

exec(𝛀().decode('zlib'))
