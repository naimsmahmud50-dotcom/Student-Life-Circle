import React from 'react';
import Link from 'next/link';
import { GraduationCap, ShieldCheck, Mail, Phone, MapPin } from 'lucide-react';

export const GoEduFooter: React.FC = () => {
  return (
    <footer className="bg-white dark:bg-gray-950 border-t border-gray-200 dark:border-gray-800 transition-colors duration-300 pt-16 pb-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-gray-100 dark:border-gray-800">
          {/* Brand & Accreditation Column */}
          <div className="lg:col-span-2 space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-full bg-[#ED8E22] flex items-center justify-center text-white shadow-md">
                <GraduationCap className="w-5 h-5" aria-hidden="true" />
              </div>
              <span className="text-xl font-black text-[#213130] dark:text-white tracking-tight">
                অগ্রযাত্রা <span className="text-[#ED8E22] text-xs font-semibold uppercase">Edu</span>
              </span>
            </Link>

            <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 leading-relaxed max-w-sm">
              বাংলাদেশের শিক্ষার্থীদের জন্য এনসিটিবি স্টেম কারিকুলাম, এডমিশন প্রেডিকশন এবং প্রফেশনাল স্কিলসের
              সমন্বিত লার্নিং প্ল্যাটফর্ম। জিইএসি স্ট্যান্ডার্ড অনুমোদিত পাঠ্যক্রম।
            </p>

            <div className="flex items-center gap-2 text-xs text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-200/60 dark:border-emerald-800/40 max-w-sm">
              <ShieldCheck className="w-4 h-4 shrink-0" aria-hidden="true" />
              <span>জিইএসি এক্রিডিটেড ও কোয়ালিটি অ্যাসিউরড সিলেবাস</span>
            </div>

            <div className="text-xs text-gray-500 dark:text-gray-400 space-y-1.5 pt-2">
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span>support@ogrojatra.edu.bd</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span>+৮৮০ ১৮১১-৪৫৮৮৩০ (সকাল ৯টা - রাত ৯টা)</span>
              </div>
            </div>
          </div>

          {/* Column 1: Learning Programs */}
          <div>
            <h3 className="font-bold text-sm text-[#213130] dark:text-white uppercase tracking-wider mb-4">
              একাডেমিক প্রোগ্রাম
            </h3>
            <ul className="space-y-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">
              <li>
                <Link href="/courses" className="hover:text-[#ED8E22] transition-colors">
                  সকল অনলাইন কোর্স
                </Link>
              </li>
              <li>
                <Link href="/courses?category=stem-math" className="hover:text-[#ED8E22] transition-colors">
                  উচ্চতর গণিত ও বিজ্ঞান
                </Link>
              </li>
              <li>
                <Link href="/courses?category=ai-tech" className="hover:text-[#ED8E22] transition-colors">
                  এআই ও টেকনোলজি
                </Link>
              </li>
              <li>
                <Link href="/admission/predictor" className="hover:text-[#ED8E22] transition-colors">
                  এডমিশন প্রেডিক্টর
                </Link>
              </li>
              <li>
                <Link href="/board-archives" className="hover:text-[#ED8E22] transition-colors">
                  বিগত ১০ বছরের বোর্ড প্রশ্ন
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 2: Interactive Features */}
          <div>
            <h3 className="font-bold text-sm text-[#213130] dark:text-white uppercase tracking-wider mb-4">
              ইন্টারেক্টিভ টুলস
            </h3>
            <ul className="space-y-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">
              <li>
                <Link href="/socratic/solver" className="hover:text-[#ED8E22] transition-colors">
                  সক্রেটিক এআই সলভার
                </Link>
              </li>
              <li>
                <Link href="/live-challenge" className="hover:text-[#ED8E22] transition-colors">
                  লাইভ চ্যালেঞ্জ এরিনা
                </Link>
              </li>
              <li>
                <Link href="/olympiad/arena" className="hover:text-[#ED8E22] transition-colors">
                  অলিম্পিয়াড এরিনা
                </Link>
              </li>
              <li>
                <Link href="/tuition" className="hover:text-[#ED8E22] transition-colors">
                  হোম টিউটর ও টিউশন হাব
                </Link>
              </li>
              <li>
                <Link href="/routines" className="hover:text-[#ED8E22] transition-colors">
                  মডেল টেস্ট ও রুটিন হাব
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Platform & Career */}
          <div>
            <h3 className="font-bold text-sm text-[#213130] dark:text-white uppercase tracking-wider mb-4">
              ক্যারিয়ার ও সাপোর্ট
            </h3>
            <ul className="space-y-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">
              <li>
                <Link href="/career/radar" className="hover:text-[#ED8E22] transition-colors">
                  ক্যারিয়ার রাডার ও জবস
                </Link>
              </li>
              <li>
                <Link href="/scholarship/disbursement" className="hover:text-[#ED8E22] transition-colors">
                  স্কলারশিপ বিতরণ
                </Link>
              </li>
              <li>
                <Link href="/study-pod" className="hover:text-[#ED8E22] transition-colors">
                  স্টাডি পড ও গ্রুপ স্টাডি
                </Link>
              </li>
              <li>
                <Link href="/viva/evaluator" className="hover:text-[#ED8E22] transition-colors">
                  ভাইভা ইভ্যালুয়েটর
                </Link>
              </li>
              <li>
                <Link href="/guardian/ptc" className="hover:text-[#ED8E22] transition-colors">
                  অভিভাবক ড্যাশবোর্ড
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-500 dark:text-gray-400 gap-4">
          <p>© ২০২৬ অগ্রযাত্রা (Student Life Circle) ও গোএডু ডিজাইন সিস্টেম। সর্বস্বত্ব সংরক্ষিত।</p>
          <div className="flex items-center gap-6">
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              গোপনীয়তা নীতি
            </Link>
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              ব্যবহারের শর্তাবলী
            </Link>
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              জিইএসি স্বীকৃতি
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
