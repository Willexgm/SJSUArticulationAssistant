from dataclasses import dataclass


@dataclass(frozen=True)
class SJSUCourse:
    prefix: str  # CS
    number: str  # 149
    title: str   # Operating Systems


@dataclass(frozen=True)
class CCCourse:
    prefix: str
    number: str
    title: str

    # def __repr__(self):
    #     return f"{self.prefix}-{self.number}"


@dataclass(frozen=True)
class GE:
    code: str  # B1
    name: str  # Physical Science

    # def __repr__(self):
    #     return self.code


@dataclass(frozen=True)
class CommunityCollege:
    full_name: str
    url_name: str

    def c_to_c_url(self):
        return f"http://transfer.sjsu.edu/web-dbgen/artic/{self.url_name}/course-to-course.html"

    def ge_url(self):
        return f"http://transfer.sjsu.edu/web-dbgen/artic/{self.url_name}/ge.html"
