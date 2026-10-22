/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Grand Public Production Launch & System Handover
 * TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
 * FILE:      frontend/src/lib/districts.ts
 * PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
 * PURPOSE:   Comprehensive 64-district inventory of Bangladesh covering all 8 administrative divisions
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
 */

export interface DistrictInfo {
  id: string;
  nameEn: string;
  nameBn: string;
  division: "Dhaka" | "Chattogram" | "Rajshahi" | "Khulna" | "Barishal" | "Sylhet" | "Rangpur" | "Mymensingh";
  activeLearners: number;
  topExamStream: string;
}

export const DISTRICTS: DistrictInfo[] = [
  // Dhaka Division (13)
  { id: "dhaka", nameEn: "Dhaka", nameBn: "ঢাকা", division: "Dhaka", activeLearners: 184500, topExamStream: "বুয়েট ও মেডিকেল ভর্তি প্রস্তুতি" },
  { id: "gazipur", nameEn: "Gazipur", nameBn: "গাজীপুর", division: "Dhaka", activeLearners: 52400, topExamStream: "ডুয়েট ও ইঞ্জিনিয়ারিং ভর্তি" },
  { id: "narayanganj", nameEn: "Narayanganj", nameBn: "নারায়ণগঞ্জ", division: "Dhaka", activeLearners: 41800, topExamStream: "এইচএসসি বিজ্ঞান বিভাগ" },
  { id: "tangail", nameEn: "Tangail", nameBn: "টাঙ্গাইল", division: "Dhaka", activeLearners: 36200, topExamStream: "মেডিকেল ভর্তি ও এইচএসসি" },
  { id: "kishoreganj", nameEn: "Kishoreganj", nameBn: "কিশোরগঞ্জ", division: "Dhaka", activeLearners: 28900, topExamStream: "বিশ্ববিদ্যালয় 'ক' ইউনিট" },
  { id: "manikganj", nameEn: "Manikganj", nameBn: "মানিকগঞ্জ", division: "Dhaka", activeLearners: 19800, topExamStream: "এইচএসসি বিজ্ঞান ও মানবিক" },
  { id: "munshiganj", nameEn: "Munshiganj", nameBn: "মুন্সীগঞ্জ", division: "Dhaka", activeLearners: 21500, topExamStream: "এসএসসি ও এইচএসসি বোর্ড আর্কাইভ" },
  { id: "narsingdi", nameEn: "Narsingdi", nameBn: "নরসিংদী", division: "Dhaka", activeLearners: 29400, topExamStream: "পাবলিক বিশ্ববিদ্যালয় ভর্তি" },
  { id: "faridpur", nameEn: "Faridpur", nameBn: "ফরিদপুর", division: "Dhaka", activeLearners: 26800, topExamStream: "মেডিকেল ও বিসিএস প্রস্তুতি" },
  { id: "gopalganj", nameEn: "Gopalganj", nameBn: "গোপালগঞ্জ", division: "Dhaka", activeLearners: 18700, topExamStream: "বিজ্ঞান ও কৃষি গুচ্ছ ভর্তি" },
  { id: "madaripur", nameEn: "Madaripur", nameBn: "মাদারীপুর", division: "Dhaka", activeLearners: 16400, topExamStream: "এইচএসসি পদার্থবিজ্ঞান ও গণিত" },
  { id: "rajbari", nameEn: "Rajbari", nameBn: "রাজবাড়ী", division: "Dhaka", activeLearners: 14200, topExamStream: "এসএসসি সাধারণ গণিত ও বিজ্ঞান" },
  { id: "shariatpur", nameEn: "Shariatpur", nameBn: "শরীয়তপুর", division: "Dhaka", activeLearners: 15100, topExamStream: "বোর্ড প্রশ্ন সমাধান ও রিভিশন" },

  // Chattogram Division (11)
  { id: "chattogram", nameEn: "Chattogram", nameBn: "চট্টগ্রাম", division: "Chattogram", activeLearners: 128900, topExamStream: "চুয়েট, চবি ও মেডিকেল ভর্তি" },
  { id: "coxs_bazar", nameEn: "Cox's Bazar", nameBn: "কক্সবাজার", division: "Chattogram", activeLearners: 24700, topExamStream: "বিশ্ববিদ্যালয় ভর্তি ও ইংরেজি দক্ষতা" },
  { id: "cumilla", nameEn: "Cumilla", nameBn: "কুমিল্লা", division: "Chattogram", activeLearners: 63800, topExamStream: "কুমিল্লা বোর্ড এসএসসি ও এইচএসসি" },
  { id: "feni", nameEn: "Feni", nameBn: "ফেনী", division: "Chattogram", activeLearners: 25400, topExamStream: "মেডিকেল ও ইঞ্জিনিয়ারিং প্রস্তুতি" },
  { id: "brahmanbaria", nameEn: "Brahmanbaria", nameBn: "ব্রাহ্মণবাড়িয়া", division: "Chattogram", activeLearners: 34100, topExamStream: "এইচএসসি রসায়ন ও উচ্চতর গণিত" },
  { id: "noakhali", nameEn: "Noakhali", nameBn: "নোয়াখালী", division: "Chattogram", activeLearners: 38700, topExamStream: "নোবিপ্রবি ও গুচ্ছ বিজ্ঞান ভর্তি" },
  { id: "lakshmipur", nameEn: "Lakshmipur", nameBn: "লক্ষ্মীপুর", division: "Chattogram", activeLearners: 19600, topExamStream: "এসএসসি ও এইচএসসি পূর্ণাঙ্গ প্রস্তুতি" },
  { id: "chandpur", nameEn: "Chandpur", nameBn: "চাঁদপুর", division: "Chattogram", activeLearners: 27900, topExamStream: "বিশ্ববিদ্যালয় 'গ' ও 'খ' ইউনিট" },
  { id: "khagrachhari", nameEn: "Khagrachhari", nameBn: "খাগড়াছড়ি", division: "Chattogram", activeLearners: 9800, topExamStream: "অনলাইন টিউটর ও স্কলারশিপ গাইড" },
  { id: "rangamati", nameEn: "Rangamati", nameBn: "রাঙ্গামাটি", division: "Chattogram", activeLearners: 11200, topExamStream: "পাবলিক বিশ্ববিদ্যালয় ও নার্সিং" },
  { id: "bandarban", nameEn: "Bandarban", nameBn: "বান্দরবান", division: "Chattogram", activeLearners: 8400, topExamStream: "দুর্যোগ-সহনশীল অফলাইন স্টাডি পড" },

  // Rajshahi Division (8)
  { id: "rajshahi", nameEn: "Rajshahi", nameBn: "রাজশাহী", division: "Rajshahi", activeLearners: 94500, topExamStream: "রুয়েট, রাবি ও মেডিকেল ভর্তি" },
  { id: "bogura", nameEn: "Bogura", nameBn: "বগুড়া", division: "Rajshahi", activeLearners: 51200, topExamStream: "মেডিকেল ও শীর্ষ কলেজ প্রস্তুতি" },
  { id: "pabna", nameEn: "Pabna", nameBn: "পাবনা", division: "Rajshahi", activeLearners: 31800, topExamStream: "পাবিপ্রবি ও এইচএসসি বিজ্ঞান" },
  { id: "sirajganj", nameEn: "Sirajganj", nameBn: "সিরাজগঞ্জ", division: "Rajshahi", activeLearners: 34600, topExamStream: "বিশ্ববিদ্যালয় 'ক' ও 'ঘ' ইউনিট" },
  { id: "naogaon", nameEn: "Naogaon", nameBn: "নওগাঁ", division: "Rajshahi", activeLearners: 23900, topExamStream: "কৃষি গুচ্ছ ও বিজ্ঞান অলিম্পিয়াড" },
  { id: "natore", nameEn: "Natore", nameBn: "নাটোর", division: "Rajshahi", activeLearners: 19400, topExamStream: "এসএসসি ও এইচএসসি পদার্থবিজ্ঞান" },
  { id: "joypurhat", nameEn: "Joypurhat", nameBn: "জয়পুরহাট", division: "Rajshahi", activeLearners: 13700, topExamStream: "গণিত ও তথ্যপ্রযুক্তি প্র্যাকটিস" },
  { id: "chapainawabganj", nameEn: "Chapainawabganj", nameBn: "চাঁপাইনবাবগঞ্জ", division: "Rajshahi", activeLearners: 18300, topExamStream: "রাবি ও গুচ্ছ ভর্তি পরীক্ষা" },

  // Khulna Division (10)
  { id: "khulna", nameEn: "Khulna", nameBn: "খুলনা", division: "Khulna", activeLearners: 78600, topExamStream: "কুয়েট, খুবি ও মেডিকেল ভর্তি" },
  { id: "jashore", nameEn: "Jashore", nameBn: "যশোর", division: "Khulna", activeLearners: 46900, topExamStream: "যবিপ্রবি ও এইচএসসি বোর্ড আর্কাইভ" },
  { id: "kushtia", nameEn: "Kushtia", nameBn: "কুষ্টিয়া", division: "Khulna", activeLearners: 32400, topExamStream: "ইবি ও বিজ্ঞান বিভাগ প্রস্তুতি" },
  { id: "jhenaidah", nameEn: "Jhenaidah", nameBn: "ঝিনাইদহ", division: "Khulna", activeLearners: 25100, topExamStream: "ক্যাডেট কলেজ ও বিশ্ববিদ্যালয় ভর্তি" },
  { id: "satkhira", nameEn: "Satkhira", nameBn: "সাতক্ষীরা", division: "Khulna", activeLearners: 22800, topExamStream: "মেডিকেল ও বিসিএস ফ্রেমওয়ার্ক" },
  { id: "bagerhat", nameEn: "Bagerhat", nameBn: "বাগেরহাট", division: "Khulna", activeLearners: 16900, topExamStream: "এইচএসসি সাধারণ ও উচ্চতর গণিত" },
  { id: "chuadanga", nameEn: "Chuadanga", nameBn: "চুয়াডাঙ্গা", division: "Khulna", activeLearners: 14800, topExamStream: "এসএসসি বিজ্ঞান ও মানবিক" },
  { id: "meherpur", nameEn: "Meherpur", nameBn: "মেহেরপুর", division: "Khulna", activeLearners: 10900, topExamStream: "অনলাইন টিউটরিং ও এসক্রো সেবা" },
  { id: "narail", nameEn: "Narail", nameBn: "নড়াইল", division: "Khulna", activeLearners: 11800, topExamStream: "গুচ্ছ ভর্তি ও স্কিল ট্রেনিং" },
  { id: "magura", nameEn: "Magura", nameBn: "মাগুরা", division: "Khulna", activeLearners: 12600, topExamStream: "বিজ্ঞান প্রশ্নব্যাংক ও সল্যুশন" },

  // Barishal Division (6)
  { id: "barishal", nameEn: "Barishal", nameBn: "বরিশাল", division: "Barishal", activeLearners: 49800, topExamStream: "ববি ও শেরেবাংলা মেডিকেল ভর্তি" },
  { id: "bhola", nameEn: "Bhola", nameBn: "ভোলা", division: "Barishal", activeLearners: 19200, topExamStream: "অফলাইন এসএমএস সিঙ্ক ও বোর্ড মক" },
  { id: "patuakhali", nameEn: "Patuakhali", nameBn: "পটুয়াখালী", division: "Barishal", activeLearners: 18700, topExamStream: "পবিপ্রবি ও কৃষি গুচ্ছ পরীক্ষা" },
  { id: "pirojpur", nameEn: "Pirojpur", nameBn: "পিরোজপুর", division: "Barishal", activeLearners: 13900, topExamStream: "এসএসসি ও এইচএসসি উচ্চতর গণিত" },
  { id: "barguna", nameEn: "Barguna", nameBn: "বরগুনা", division: "Barishal", activeLearners: 11400, topExamStream: "দুর্যোগ সহনশীল শিক্ষাসেবা" },
  { id: "jhalokathi", nameEn: "Jhalokathi", nameBn: "ঝালকাঠি", division: "Barishal", activeLearners: 10200, topExamStream: "পাবলিক বিশ্ববিদ্যালয় ও বিসিএস" },

  // Sylhet Division (4)
  { id: "sylhet", nameEn: "Sylhet", nameBn: "সিলেট", division: "Sylhet", activeLearners: 71200, topExamStream: "শাবিপ্রবি, ওসমানী মেডিকেল ও আইইএলটিএস" },
  { id: "moulvibazar", nameEn: "Moulvibazar", nameBn: "মৌলভীবাজার", division: "Sylhet", activeLearners: 26800, topExamStream: "বিশ্ববিদ্যালয় বিজ্ঞান ও ব্যবসায় শিক্ষা" },
  { id: "habiganj", nameEn: "Habiganj", nameBn: "হবিগঞ্জ", division: "Sylhet", activeLearners: 23400, topExamStream: "কৃষি ও প্রকৌশল গুচ্ছ ভর্তি" },
  { id: "sunamganj", nameEn: "Sunamganj", nameBn: "সুনামগঞ্জ", division: "Sylhet", activeLearners: 19500, topExamStream: "হাওর অঞ্চল অফলাইন রিভিশন নেটওয়ার্ক" },

  // Rangpur Division (8)
  { id: "rangpur", nameEn: "Rangpur", nameBn: "রংপুর", division: "Rangpur", activeLearners: 64700, topExamStream: "বেগম রোকেয়া বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি" },
  { id: "dinajpur", nameEn: "Dinajpur", nameBn: "দিনাজপুর", division: "Rangpur", activeLearners: 41200, topExamStream: "হাবিপ্রবি ও দিনাজপুর বোর্ড আর্কাইভ" },
  { id: "gaibandha", nameEn: "Gaibandha", nameBn: "গাইবান্ধা", division: "Rangpur", activeLearners: 22600, topExamStream: "বিশ্ববিদ্যালয় গুচ্ছ ও নার্সিং" },
  { id: "kurigram", nameEn: "Kurigram", nameBn: "কুড়িগ্রাম", division: "Rangpur", activeLearners: 18900, topExamStream: "চরম জলবায়ু অফলাইন লার্নিং ভল্ট" },
  { id: "lalmonirhat", nameEn: "Lalmonirhat", nameBn: "লালমনিরহাট", division: "Rangpur", activeLearners: 14700, topExamStream: "এসএসসি ও এইচএসসি মডেল টেস্ট" },
  { id: "nilphamari", nameEn: "Nilphamari", nameBn: "নীলফামারী", division: "Rangpur", activeLearners: 19800, topExamStream: "মেডিকেল ও বিসিএস প্রস্তুতি" },
  { id: "panchagarh", nameEn: "Panchagarh", nameBn: "পঞ্চগড়", division: "Rangpur", activeLearners: 13500, topExamStream: "বিজ্ঞান ও সাধারণ জ্ঞান কুইজ" },
  { id: "thakurgaon", nameEn: "Thakurgaon", nameBn: "ঠাকুরগাঁও", division: "Rangpur", activeLearners: 17600, topExamStream: "কৃষি বিশ্ববিদ্যালয় ও প্রকৌশল ভর্তি" },

  // Mymensingh Division (4)
  { id: "mymensingh", nameEn: "Mymensingh", nameBn: "ময়মনসিংহ", division: "Mymensingh", activeLearners: 68900, topExamStream: "বাকৃবি ও ময়মনসিংহ মেডিকেল ভর্তি" },
  { id: "jamalpur", nameEn: "Jamalpur", nameBn: "জামালপুর", division: "Mymensingh", activeLearners: 27400, topExamStream: "বঙ্গমাতা ফজিলাতুন্নেছা মুজিব বিশ্ববিদ্যালয় ভর্তি" },
  { id: "netrokona", nameEn: "Netrokona", nameBn: "নেত্রকোণা", division: "Mymensingh", activeLearners: 21600, topExamStream: "নেত্রকোণা বিশ্ববিদ্যালয় ও এইচএসসি" },
  { id: "sherpur", nameEn: "Sherpur", nameBn: "শেরপুর", division: "Mymensingh", activeLearners: 16800, topExamStream: "বোর্ড প্রশ্নব্যাংক ও ক্যারিয়ার রাডার" }
];

export const getDistrictById = (id: string): DistrictInfo | undefined => {
  const cleanId = id.toLowerCase().replace(/[-\s]/g, "_");
  return DISTRICTS.find((d) => d.id === cleanId);
};

export const getAllDistricts = (): DistrictInfo[] => {
  return DISTRICTS;
};

export const getDistrictsByDivision = (division: string): DistrictInfo[] => {
  return DISTRICTS.filter((d) => d.division.toLowerCase() === division.toLowerCase());
};
