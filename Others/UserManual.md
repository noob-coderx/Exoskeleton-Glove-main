# MIRAGE  
### *Motion Integrated Real-time Articulated Glove Emulator*

---

## Mechanical Assembly

Each mechanical joint in this system corresponds to a biological joint and is named accordingly. The assembly supports **12 Degrees of Freedom (DoF)**.

### Naming Convention

Each DoF in a finger is labeled as `x.1`, `x.2`, `x.3`, where:
- `x` is the finger ID
- The digits represent the joint's position from top to bottom

#### Finger Indexing
| Finger         | ID |
|----------------|----|
| Index Finger   | 1  |
| Middle Finger  | 2  |
| Ring Finger    | 3  |
| Pinky Finger   | 4  *(only 2 joints)* |
| Thumb          | 5  *(only 1 joint tracked)* |

#### Example
For the index finger:
- `1.1` → Top joint  
- `1.2` → Middle joint  
- `1.3` → Bottom joint

---

## Joint-to-Circuit Board Mapping

Use the following mapping for correct wiring between joints and the circuit board:

| Joint | Circuit Pin |  | Joint | Circuit Pin |
|-------|--------------|--|--------|-------------|
| 1.1   | C4           |  | 3.1    | C10         |
| 1.2   | C5           |  | 3.2    | C11         |
| 1.3   | C6           |  | 3.3    | C12         |
| 2.1   | C7           |  | 4.1    | C13         |
| 2.2   | C8           |  | 4.2    | C14         |
| 2.3   | C9           |  | 5.1    | C15         |

---

## Initialization Modes

### 1. **Auto-Calibration Mode**
- **Phase 1**: Keep all fingers **as straight as possible**.
- **Phase 2**: Form a **fist** (or as close to one as possible).
- The system will automatically calibrate based on these two hand postures.

### 2. **Manual-Calibration Mode**
- Involves only **one phase of calibration**.
- Uses a **default sensitivity** which can be **manually adjusted** for more accurate joint angle readings.

---

> Tip: For best results, ensure consistent posture during calibration and check sensor alignment if unexpected readings occur.
