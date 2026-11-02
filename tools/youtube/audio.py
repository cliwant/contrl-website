"""Synthesize background music + sound effects for the YouTube cut (contrl-youtube-ko.mp4).

Everything is generated here (no samples), so the track is free of licensing issues.
Event times are in the final video's timeline; see the anchor tables below.
Usage: python3 audio.py out.wav
"""
import sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
TOTAL = 114.2
rng = np.random.default_rng(7)

# ---------- timeline mapping (page time → final video time) ----------
# Problem video (segment A starts at 0): anchors fitted from caption onsets and card fades.
A_PAGE = [0.0, 4.84, 10.47, 12.81, 17.44, 20.24, 23.86, 27.46, 31.06, 46.0, 48.9, 60.0]
A_VID = [0.0, 4.88, 11.17, 13.92, 19.0, 22.0, 25.92, 29.75, 33.62, 49.4, 52.4, 63.5]
def pa(t): return float(np.interp(t, A_PAGE, A_VID))

# Contrl demo (segment C starts at 60.333 in the final cut, trimmed from 0.8s).
C0 = 60.333
C_PAGE = [0.8, 1.92, 17.12, 25.38, 37.94, 50.0]
C_VID = [0.0, 1.29, 16.67, 25.83, 39.75, 51.9]
def pc(t): return C0 + float(np.interp(t, C_PAGE, C_VID))

BRIDGE = 57.633      # crossfade into the bridge card
END_CARD = 108.633   # crossfade into the end card

# ---------- helpers ----------
def n(sec): return int(round(sec * SR))
def buf(): return np.zeros((n(TOTAL), 2))

def place(track, sig, t, gain=1.0, pan=0.0):
    if sig.ndim == 1: sig = np.stack([sig, sig], 1)
    l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
    sig = sig * np.array([l * 1.414, r * 1.414]) * gain
    i = n(t)
    if i >= len(track): return
    j = min(len(track), i + len(sig))
    track[i:j] += sig[: j - i]

def env_adsr(length, a=0.01, d=0.1, s=0.7, r=0.2):
    N = n(length); e = np.ones(N) * s
    A, D, R = n(a), n(d), n(r)
    e[:A] = np.linspace(0, 1, A, endpoint=False)
    e[A:A + D] = np.linspace(1, s, D, endpoint=False)[: max(0, min(D, N - A))]
    if R: e[-R:] *= np.linspace(1, 0, R)
    return e

def lowpass(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'low'); return signal.lfilter(b, a, x)
def highpass(x, fc, order=2):
    b, a = signal.butter(order, fc / (SR / 2), 'high'); return signal.lfilter(b, a, x)
def bandpass(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band'); return signal.lfilter(b, a, x)

def reverb(x, sec=1.8, mix=0.25):
    """Short convolution reverb — fine for transients (SFX)."""
    ir_n = n(sec); ir = rng.standard_normal(ir_n) * np.exp(-np.linspace(0, 6, ir_n))
    ir = lowpass(ir, 6000); ir /= np.sqrt((ir ** 2).sum())
    out = np.stack([signal.fftconvolve(x[:, c], ir)[: len(x)] for c in range(2)], 1)
    return x * (1 - mix) + out * mix

def space(x, mix=0.3):
    """Smooth multi-tap echo for the sustained music bed (no resonant peaks)."""
    out = np.zeros_like(x)
    taps = [(0.047, 0.30, 0.2), (0.083, 0.26, -0.3), (0.121, 0.22, 0.35), (0.167, 0.18, -0.25),
            (0.229, 0.14, 0.15), (0.311, 0.10, -0.1), (0.419, 0.07, 0.3), (0.557, 0.05, -0.3)]
    for d, g, pan in taps:
        k = n(d); l, r = g * (1 - pan) / 1.0, g * (1 + pan) / 1.0
        out[k:, 0] += x[:-k, 0] * l; out[k:, 1] += x[:-k, 1] * r
    out = np.stack([lowpass(out[:, c], 4500) for c in range(2)], 1)
    return x * (1 - mix * 0.5) + out * mix

def note(m): return 440.0 * 2 ** ((m - 69) / 12)

# ---------- instruments ----------
def pad(midis, length, bright=1800, vol=0.12):
    t = np.arange(n(length)) / SR; out = np.zeros(len(t))
    for m in midis:
        for det in (-0.08, 0.0, 0.07):
            f = note(m) * 2 ** (det / 12)
            out += signal.sawtooth(2 * np.pi * f * t + rng.uniform(0, 6.28))
    out = lowpass(out / (3 * len(midis)), bright, 2)
    return out * env_adsr(length, 0.8, 0.5, 0.85, 1.2) * vol

def pluck(m, length=1.2, vol=0.18, bright=0.5):
    f = note(m); p = max(2, int(SR / f)); N = n(length)
    buf_ = rng.uniform(-1, 1, p); out = np.zeros(N)
    for i in range(N):
        out[i] = buf_[i % p]
        buf_[i % p] = bright * (buf_[i % p] + buf_[(i + 1) % p]) + (1 - 2 * bright) * buf_[i % p] if False else 0.499 * (buf_[i % p] + buf_[(i + 1) % p])
    return lowpass(out, 5000) * vol * np.exp(-np.linspace(0, 3, N))

def kick(vol=0.5):
    N = n(0.35); t = np.arange(N) / SR
    f = 45 + 80 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * vol

def hat(vol=0.06, length=0.05):
    N = n(length); return highpass(rng.standard_normal(N), 7000) * np.exp(-np.linspace(0, 8, N)) * vol

def bass(m, length, vol=0.22):
    t = np.arange(n(length)) / SR; f = note(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return lowpass(x, 400) * env_adsr(length, 0.02, 0.2, 0.7, 0.15) * vol

# ---------- SFX ----------
def pop(f=880, vol=0.35):
    N = n(0.12); t = np.arange(N) / SR
    fr = f * (1 + 0.6 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 35) * vol

def click(vol=0.25):
    N = n(0.02); return bandpass(rng.standard_normal(N), 2000, 9000) * np.exp(-np.linspace(0, 10, N)) * vol

def typing(length, rate=14, vol=0.16):
    out = np.zeros(n(length) + n(0.05)); t = 0.0
    while t < length:
        c = click(vol * rng.uniform(0.6, 1.0)); i = n(t); out[i:i + len(c)] += c
        t += rng.uniform(0.6, 1.4) / rate
    return out

def whoosh(length=0.6, lo=300, hi=4000, vol=0.3, rising=True):
    N = n(length); x = rng.standard_normal(N); out = np.zeros(N); seg = 512
    for s in range(0, N, seg):
        k = s / N; k = k if rising else 1 - k
        fc = lo * (hi / lo) ** k
        out[s:s + seg] = bandpass(x[s:s + seg + 0][: seg], max(60, fc * 0.6), min(SR / 2 - 100, fc * 1.4), 1)
    e = np.sin(np.linspace(0, np.pi, N)) ** 1.5
    return lowpass(out, 9000) * e * vol

def chime(m=84, vol=0.25, length=2.2):
    N = n(length); t = np.arange(N) / SR; f = note(m); out = np.zeros(N)
    for k, a in ((1, 1), (2.76, 0.35), (5.4, 0.15), (2.0, 0.25)):
        out += a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (2.2 + k * 0.8))
    return out * vol

def alert(vol=0.22):  # two-note "flag" ping
    a = chime(76, 1, 0.5); b = chime(72, 1, 0.7); out = np.zeros(n(0.8))
    out[: len(a)] += a; out[n(0.12): n(0.12) + len(b)] += b[: len(out) - n(0.12)]
    return out * vol

def boom(vol=0.6):
    N = n(2.6); t = np.arange(N) / SR
    low = np.sin(2 * np.pi * (38 + 30 * np.exp(-t * 6)) * t) * np.exp(-t * 1.6)
    noise = lowpass(rng.standard_normal(N), 300) * np.exp(-t * 4) * 0.5
    return (low + noise) * vol

def riser(length=1.2, vol=0.18):
    return whoosh(length, 400, 7000, vol, rising=True) * np.linspace(0.3, 1, n(length))

def ticks(length, count, vol=0.07, f0=1400, f1=2600):
    out = np.zeros(n(length) + n(0.13))
    for k in range(count):
        tt = length * (k / count) ** 0.8; p = pop(f0 + (f1 - f0) * k / count, vol)
        i = n(tt); out[i:i + len(p)] += p
    return out

# ---------- music ----------
def music():
    mus = buf()
    beat = 60 / 100

    # Part 1: tense A-minor bed under the generic-tool story (0 → end card)
    prog1 = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    bass1 = [45, 41, 36, 43]
    t, i = 0.0, 0
    while t < 49.0:
        bar = beat * 4
        place(mus, pad(prog1[i % 4], bar + 1.0, 1400, 0.10), t)
        place(mus, bass(bass1[i % 4], bar * 0.95, 0.16), t)
        if t > 4.5:  # rhythm comes in after the opening card
            for b in range(4):
                place(mus, kick(0.28 if b in (0, 2) else 0.0), t + b * beat)
                place(mus, hat(0.035), t + b * beat + beat / 2, pan=0.3)
            if t > 34:  # more tension in the Slack part
                for b in range(8): place(mus, hat(0.03), t + b * beat / 2, pan=-0.3)
        t += bar; i += 1

    # Resolve: bright swell on the Contrl card (52.4) through the bridge
    place(mus, pad([60, 64, 67, 72], 8.5, 3200, 0.13), 52.2)
    place(mus, bass(36, 8.0, 0.14), 52.4)

    # Part 2: hopeful C-major groove under the Contrl demo
    prog2 = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]  # C G Am F
    bass2 = [36, 43, 45, 41]
    arp = [0, 2, 1, 2]
    t, i = C0 - 0.2, 0
    while t < END_CARD + 0.2:
        bar = beat * 4; ch = prog2[i % 4]
        place(mus, pad(ch, bar + 1.0, 2600, 0.085), t)
        place(mus, bass(bass2[i % 4], bar * 0.95, 0.15), t)
        for b in range(8):
            place(mus, pluck(ch[arp[b % 4]] + 12, 0.9, 0.09), t + b * beat / 2, pan=(-0.25 if b % 2 else 0.25))
        for b in range(4):
            place(mus, kick(0.24 if b in (0, 2) else 0.0), t + b * beat)
            place(mus, hat(0.03), t + b * beat + beat / 2, pan=0.3)
        t += bar; i += 1

    # Outro: final chord under the end card
    place(mus, pad([48, 60, 64, 67, 72], 6.0, 3000, 0.13), END_CARD - 0.2)
    place(mus, chime(84, 0.18, 4.0), END_CARD + 0.4)
    place(mus, chime(91, 0.10, 3.5), END_CARD + 0.55)

    # duck the music under the dark "too much" card (silence before the reveal)
    e = np.ones(len(mus)); a, b = n(49.2), n(52.2)
    e[a:b] = np.concatenate([np.linspace(1, 0.15, n(0.4)), np.full(b - a - n(0.4), 0.15)])
    # fade in / out
    e[: n(1.5)] *= np.linspace(0, 1, n(1.5)); e[-n(2.5):] *= np.linspace(1, 0, n(2.5))
    return mus * e[:, None]

# ---------- SFX timeline ----------
def sfx():
    fx = buf()
    # opening card: tag + chips pop in
    place(fx, pop(660, 0.18), 1.1)
    for k, d in enumerate((0.35, 0.5, 0.65, 0.8)):
        place(fx, pop(900 + 120 * k, 0.22), pa(1.04 + d), pan=-0.4 + 0.27 * k)
    # files dragged and dropped
    place(fx, whoosh(0.5, 300, 2500, 0.18), pa(7.85))
    for k in range(6): place(fx, pop(1100 + 60 * k, 0.12), pa(8.30 + 0.11 * k), pan=-0.3 + 0.12 * k)
    # prompt typed, generate clicked
    place(fx, typing(pa(11.13) - pa(10.47) + 0.1, 16, 0.14), pa(10.47))
    place(fx, click(0.4), pa(11.94)); place(fx, pop(520, 0.2), pa(11.94) + 0.02)
    # 100 thumbnails pour in
    place(fx, ticks(pa(15.06) - pa(12.79), 40, 0.05), pa(12.79))
    # zoom to slide 12
    place(fx, whoosh(0.7, 250, 3500, 0.2), pa(16.18) - 0.2)
    # the four flagged problems
    for tt in (19.44, 23.04, 26.64, 30.25): place(fx, alert(0.2), pa(tt))
    # Slack: window, messages, typing indicator
    place(fx, whoosh(0.5, 400, 3000, 0.15), pa(34.71) - 0.15)
    for tt in (35.61, 37.11, 39.41, 41.11): place(fx, pop(1250, 0.2), pa(tt)); place(fx, pop(1650, 0.12), pa(tt) + 0.06)
    place(fx, typing(1.0, 9, 0.08), pa(38.21))
    # "too much" impact, then the Contrl reveal
    place(fx, boom(0.55), 49.35)
    place(fx, riser(1.4, 0.16), 51.0)
    place(fx, chime(79, 0.22, 2.5), 52.4); place(fx, chime(84, 0.14, 2.5), 52.55)
    # bridge card
    place(fx, whoosh(0.9, 300, 5000, 0.18), BRIDGE - 0.3)
    place(fx, whoosh(0.7, 5000, 300, 0.12, rising=False), C0 - 0.35)

    # Contrl demo
    for tt in (4.92, 7.5, 10.92, 13.43, 15.9, 19.33, 21.73, 24.17, 27.6, 34.03, 37.15, 39.95):
        place(fx, pop(980, 0.14), pc(tt), pan=0.3)
    for tt, ln in ((6.62, 1.6), (15.02, 1.2), (23.33, 1.2), (35.83, 1.5)):
        place(fx, typing(ln, 15, 0.10), pc(tt))
    for tt in (9.31, 17.73, 25.99):  # Win Theme / key sentence / plan picked
        place(fx, click(0.35), pc(tt)); place(fx, chime(81, 0.16, 1.4), pc(tt) + 0.05)
    for tt in (12.02, 20.33, 28.5):  # next step
        place(fx, whoosh(0.55, 400, 4000, 0.13), pc(tt) - 0.2)
    place(fx, ticks(1.6, 17, 0.06, 1500, 2700), pc(29.4))   # 17 slides written
    place(fx, chime(84, 0.2, 2.0), pc(32.02)); place(fx, chime(88, 0.12, 2.0), pc(32.02) + 0.12)
    place(fx, whoosh(0.6, 400, 4500, 0.14), pc(37.94) - 0.2)  # rewrite page 1
    place(fx, chime(86, 0.16, 1.8), pc(39.34)); place(fx, chime(91, 0.08, 1.6), pc(39.34) + 0.1)

    # end card
    place(fx, whoosh(0.8, 300, 5000, 0.16), END_CARD - 0.3)
    return fx

def main(out):
    mus = space(music(), 0.35)
    fx = reverb(sfx(), 1.2, 0.18)
    mix = mus * 0.9 + fx
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)  # gentle soft clip
    mix /= max(1e-9, np.abs(mix).max()) / 0.89
    wavfile.write(out, SR, (mix * 32767).astype(np.int16))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'mix.wav')
