# akc-point-tracker

## Architecture

### Dog Table

ID (Int, PK)
Name
Show Name
Points (Int)
Season Points
Owner's Name
Actions (Update | Delete)
Deleted (Boolean)

### Titles Table

ID (Int, PK)
Show Name (FK)
MACH
AGCH

### Owner Table

ID (Int, PK)
Name
Actions (Update | Delete)
Deleted (Boolean)

### Runs Table

Date
Judge
Place
Run Time
Course Time
Qualified
Points Earned
Trial Club
Jump Height
Actions (Update | Delete)
Deleted (Boolean)
