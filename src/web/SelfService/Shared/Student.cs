using System;
using System.Collections.Generic;
using System.Text;

namespace SelfService.Shared
{
    public class Student
    {
        public string Name { get; set; }
        public string Id {get; set;}
        public string Grade {get; set;}
        public string Phone {get; set;}
        public string Email {get; set;}
        public string GithubUrl {get; set;}
        public string Location {get; set;}
        public string Notes {get; set;}
        public ProfileResource Profile {get; set;}
    }
}
