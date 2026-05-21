from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class CMRData:
    sender: str = ""
    consignee: str = ""
    delivery_address: str = ""
    carrier: str = ""
    place_date_taking_over: str = ""
    successive_carriers: str = ""
    place_designated_delivery: str = ""
    marks_numbers: str = ""
    number_kind_packages: str = ""
    description_goods: str = ""
    gross_weight: str = ""
    volume: str = ""
    carriage_charges: str = ""
    customs_instructions: str = ""
    t_form_instructions: str = ""
    reservations: str = ""
    documents_attached: str = ""
    special_agreements: str = ""
    goods_received: str = ""
    goods_collected: str = ""
    wh_job_reference: str = ""
    place_date: str = ""
    signatures_stamps: str = ""
    company_completing_note: str = ""

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "CMRData":
        known = {field: data.get(field, "") for field in cls.__annotations__.keys()}
        return cls(**known)


REQUIRED_FIELDS = [
    "sender",
    "consignee",
    "carrier",
    "place_date_taking_over",
    "description_goods",
]

FIELD_LABELS = {
    "sender": "1. Sender / Expéditeur",
    "consignee": "2. Consignee / Destinataire",
    "delivery_address": "3. Delivery address / Adresse de livraison",
    "carrier": "4. Carrier / Transporteur",
    "place_date_taking_over": "5. Place and date of taking over / Lieu et date de prise en charge",
    "successive_carriers": "6. Successive carriers / Transporteurs successifs",
    "place_designated_delivery": "7. Place designated for delivery / Lieu prévu pour la livraison",
    "marks_numbers": "8. Marks and numbers / Marques et numéros",
    "number_kind_packages": "9. Number and kind of packages / Nombre et nature des colis",
    "description_goods": "10. Description of goods / Nature de la marchandise",
    "gross_weight": "11. Gross weight / Poids brut (kg)",
    "volume": "12. Volume (m³)",
    "carriage_charges": "13. Carriage charges / Frais de transport",
    "customs_instructions": "14. Sender’s customs instructions / Instructions douanières",
    "t_form_instructions": "15. T-form instructions",
    "reservations": "16. Reservations / Réserves",
    "documents_attached": "17. Documents attached / Documents annexés",
    "special_agreements": "18. Special agreements / Conventions particulières",
    "goods_received": "19. Goods received / Marchandises reçues",
    "goods_collected": "20. Goods collected / Marchandises collectées",
    "wh_job_reference": "21. WH job reference",
    "place_date": "22. Place and date / Lieu et date",
    "signatures_stamps": "23. Signature/stamp areas / Signatures et cachets",
    "company_completing_note": "24. Company completing this note",
}

MULTILINE_FIELDS = {
    "sender",
    "consignee",
    "delivery_address",
    "carrier",
    "successive_carriers",
    "description_goods",
    "customs_instructions",
    "reservations",
    "documents_attached",
    "special_agreements",
    "goods_received",
    "goods_collected",
    "signatures_stamps",
    "company_completing_note",
}
