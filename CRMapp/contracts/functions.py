from CRMapp.models import *
from django.utils import timezone

def move_to_next_phase(contract):
    current_phase = Phase.objects.filter(contract=contract, isActive=True).first()

    if current_phase:
        current_phase.isActive = False
        current_phase.end_date = timezone.now()
        current_phase.save()

        current_phase_name = current_phase.Name
        next_phase_name = None
        for i, phase in enumerate(PHASES_NAME):
            if phase[1] == current_phase_name:
                if i + 1 < len(PHASES_NAME):
                    next_phase_name = PHASES_NAME[i + 1][1]
                break

        if next_phase_name:
            new_phase = Phase.objects.create(
                client=contract.client,
                contract=contract,
                Name=next_phase_name,
                isActive=True,
                start_date=timezone.now(),
            )
            return new_phase

    return None       


def move_to_specific_phase(contract,start_date, new_phase_name):
    # التحقق مما إذا كان اسم المرحلة المُدخل موجود ضمن الـ PHASES_NAME
    if new_phase_name not in [choice[1] for choice in PHASES_NAME]:
        return None  
    if Phase.objects.filter(contract=contract).count()==0:
        return None
    
    current_phase = Phase.objects.filter(contract=contract, isActive=True).first()

    if current_phase:
        current_phase.isActive = False
        current_phase.end_date = timezone.now()
        current_phase.save()

    new_phase = Phase.objects.create(
        client=contract.client,
        contract=contract,
        Name=new_phase_name,
        isActive=True,
        start_date=start_date,
    )
    return new_phase

   